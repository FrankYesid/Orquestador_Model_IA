"""
Script para crear una base de datos dummy con datos de ventas simulados.
Este script genera datos de ejemplo para demostrar el flujo ETL.
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.db_config import db_config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()


def generate_dummy_data(num_records=1000):
    """
    Genera datos dummy de ventas para la demostración.
    
    Args:
        num_records (int): Número de registros a generar
        
    Returns:
        pd.DataFrame: DataFrame con los datos generados
    """
    logger.info(f"Generando {num_records} registros de datos dummy...")
    
    # Configurar semilla para reproducibilidad
    np.random.seed(42)
    
    # Generar fechas
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(num_records)]
    
    # Productos y categorías
    products = ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Webcam', 
                'Auriculares', 'Tablet', 'Smartphone', 'Impresora', 'Router']
    categories = ['Electrónica', 'Accesorios', 'Computadoras', 'Redes']
    regions = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
    
    # Generar datos
    data = {
        'id': range(1, num_records + 1),
        'fecha': np.random.choice(dates, num_records),
        'producto': np.random.choice(products, num_records),
        'categoria': np.random.choice(categories, num_records),
        'region': np.random.choice(regions, num_records),
        'cantidad': np.random.randint(1, 50, num_records),
        'precio_unitario': np.round(np.random.uniform(10.0, 1500.0, num_records), 2),
        'descuento': np.round(np.random.uniform(0.0, 0.3, num_records), 2),
        'cliente_id': np.random.randint(1000, 9999, num_records),
        'vendedor_id': np.random.randint(1, 50, num_records)
    }
    
    df = pd.DataFrame(data)
    
    # Calcular total de venta
    df['total_venta'] = df['cantidad'] * df['precio_unitario'] * (1 - df['descuento'])
    df['total_venta'] = df['total_venta'].round(2)
    
    # Agregar algunos valores nulos para demostrar limpieza de datos
    null_indices = np.random.choice(df.index, size=int(num_records * 0.02), replace=False)
    df.loc[null_indices, 'descuento'] = np.nan
    
    logger.info(f"Datos generados exitosamente: {df.shape}")
    return df


def create_database_tables():
    """
    Crea las tablas necesarias en la base de datos.
    """
    logger.info("Creando tablas en la base de datos...")
    
    # Tabla de datos fuente (sales_data)
    create_source_table = f"""
    CREATE TABLE IF NOT EXISTS {db_config.table_source} (
        id INTEGER PRIMARY KEY,
        fecha TEXT NOT NULL,
        producto TEXT NOT NULL,
        categoria TEXT,
        region TEXT,
        cantidad INTEGER,
        precio_unitario REAL,
        descuento REAL,
        total_venta REAL,
        cliente_id INTEGER,
        vendedor_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    # Tabla de datos transformados (sales_transformed)
    create_target_table = f"""
    CREATE TABLE IF NOT EXISTS {db_config.table_target} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        producto TEXT NOT NULL,
        categoria TEXT,
        region TEXT,
        cantidad_total INTEGER,
        precio_promedio REAL,
        descuento_promedio REAL,
        total_venta REAL,
        num_transacciones INTEGER,
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    try:
        db_config.execute_query(create_source_table)
        logger.info(f"Tabla '{db_config.table_source}' creada exitosamente")
        
        db_config.execute_query(create_target_table)
        logger.info(f"Tabla '{db_config.table_target}' creada exitosamente")
    except Exception as e:
        logger.error(f"Error creando tablas: {e}")
        raise


def insert_dummy_data(df):
    """
    Inserta los datos dummy en la tabla de origen.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos a insertar
    """
    logger.info("Insertando datos en la base de datos...")
    
    conn = db_config.get_connection()
    
    try:
        # Convertir fecha a string para SQLite
        df['fecha'] = df['fecha'].astype(str)
        
        # Insertar datos
        df.to_sql(
            db_config.table_source,
            conn,
            if_exists='replace',
            index=False
        )
        
        logger.info(f"{len(df)} registros insertados en '{db_config.table_source}'")
    except Exception as e:
        logger.error(f"Error insertando datos: {e}")
        raise
    finally:
        db_config.close_connection(conn)


def save_sample_csv(df, output_path=None):
    """
    Guarda una muestra de los datos en CSV para referencia.
    
    Args:
        df (pd.DataFrame): DataFrame a guardar
        output_path (str, optional): Ruta donde guardar el CSV
    """
    if output_path is None:
        output_path = os.getenv('DATA_INPUT_PATH', 'data/input')
    
    # Crear directorio si no existe
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    csv_path = os.path.join(output_path, 'dummy_data.csv')
    df.to_csv(csv_path, index=False)
    logger.info(f"Datos de muestra guardados en: {csv_path}")


def main():
    """
    Función principal que ejecuta todo el proceso de creación de la BD dummy.
    """
    logger.info("=" * 60)
    logger.info("INICIANDO CREACIÓN DE BASE DE DATOS DUMMY")
    logger.info("=" * 60)
    
    try:
        # 1. Generar datos dummy
        df = generate_dummy_data(num_records=1000)
        
        # 2. Crear tablas
        create_database_tables()
        
        # 3. Insertar datos
        insert_dummy_data(df)
        
        # 4. Guardar CSV de muestra
        save_sample_csv(df)
        
        # 5. Verificar datos insertados
        conn = db_config.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {db_config.table_source}")
        count = cursor.fetchone()[0]
        db_config.close_connection(conn)
        
        logger.info("=" * 60)
        logger.info(f"✓ Base de datos creada exitosamente")
        logger.info(f"✓ Total de registros en BD: {count}")
        logger.info(f"✓ Ubicación: {db_config.db_path}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Error en el proceso: {e}")
        raise


if __name__ == "__main__":
    main()
