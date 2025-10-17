"""
Script de Extracción (Extract) del proceso ETL.
Extrae datos desde la base de datos SQLite y los prepara para transformación.
"""

import pandas as pd
import sqlite3
import os
import sys
from pathlib import Path
from datetime import datetime
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


def extract_data_from_db(table_name=None, date_filter=None, limit=None):
    """
    Extrae datos desde la base de datos SQLite.
    
    Args:
        table_name (str, optional): Nombre de la tabla a extraer
        date_filter (str, optional): Filtro de fecha en formato 'YYYY-MM-DD'
        limit (int, optional): Límite de registros a extraer
        
    Returns:
        pd.DataFrame: DataFrame con los datos extraídos
    """
    if table_name is None:
        table_name = db_config.table_source
    
    logger.info(f"Iniciando extracción de datos desde tabla: {table_name}")
    
    # Construir query SQL
    query = f"SELECT * FROM {table_name}"
    
    # Agregar filtros si existen
    conditions = []
    if date_filter:
        conditions.append(f"fecha >= '{date_filter}'")
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    # Agregar límite si existe
    if limit:
        query += f" LIMIT {limit}"
    
    logger.info(f"Ejecutando query: {query}")
    
    try:
        # Conectar y extraer datos
        conn = db_config.get_connection()
        df = pd.read_sql_query(query, conn)
        db_config.close_connection(conn)
        
        logger.info(f"✓ Datos extraídos exitosamente: {df.shape[0]} filas, {df.shape[1]} columnas")
        
        # Mostrar información básica
        logger.info(f"Columnas: {list(df.columns)}")
        logger.info(f"Rango de fechas: {df['fecha'].min()} a {df['fecha'].max()}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error extrayendo datos: {e}")
        raise


def validate_extracted_data(df):
    """
    Valida los datos extraídos antes de continuar con el proceso.
    
    Args:
        df (pd.DataFrame): DataFrame a validar
        
    Returns:
        bool: True si los datos son válidos
    """
    logger.info("Validando datos extraídos...")
    
    validations = []
    
    # 1. Verificar que no esté vacío
    if df.empty:
        logger.error("❌ El DataFrame está vacío")
        validations.append(False)
    else:
        logger.info(f"✓ DataFrame contiene {len(df)} registros")
        validations.append(True)
    
    # 2. Verificar columnas requeridas
    required_columns = ['id', 'fecha', 'producto', 'cantidad', 'precio_unitario', 'total_venta']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        logger.error(f"❌ Columnas faltantes: {missing_columns}")
        validations.append(False)
    else:
        logger.info("✓ Todas las columnas requeridas están presentes")
        validations.append(True)
    
    # 3. Verificar tipos de datos básicos
    try:
        df['fecha'] = pd.to_datetime(df['fecha'])
        logger.info("✓ Columna 'fecha' convertida a datetime")
        validations.append(True)
    except Exception as e:
        logger.error(f"❌ Error convirtiendo fechas: {e}")
        validations.append(False)
    
    # 4. Verificar valores numéricos
    numeric_columns = ['cantidad', 'precio_unitario', 'total_venta']
    for col in numeric_columns:
        if col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                logger.warning(f"⚠ Columna '{col}' no es numérica, intentando conversión...")
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    validations.append(True)
                except:
                    validations.append(False)
    
    # 5. Reportar valores nulos
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        logger.warning("⚠ Valores nulos encontrados:")
        for col, count in null_counts[null_counts > 0].items():
            logger.warning(f"  - {col}: {count} valores nulos ({count/len(df)*100:.2f}%)")
    else:
        logger.info("✓ No se encontraron valores nulos")
    
    # Resultado final
    is_valid = all(validations)
    if is_valid:
        logger.info("✓ Validación completada exitosamente")
    else:
        logger.error("❌ Validación falló")
    
    return is_valid


def save_extracted_data(df, output_path=None, filename='extracted_data.csv'):
    """
    Guarda los datos extraídos en un archivo CSV temporal.
    
    Args:
        df (pd.DataFrame): DataFrame a guardar
        output_path (str, optional): Ruta donde guardar el archivo
        filename (str): Nombre del archivo
    """
    if output_path is None:
        output_path = os.getenv('DATA_OUTPUT_PATH', 'data/output')
    
    # Crear directorio si no existe
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # Ruta completa del archivo
    file_path = os.path.join(output_path, filename)
    
    try:
        df.to_csv(file_path, index=False)
        logger.info(f"✓ Datos extraídos guardados en: {file_path}")
        logger.info(f"  Tamaño del archivo: {os.path.getsize(file_path) / 1024:.2f} KB")
    except Exception as e:
        logger.error(f"Error guardando datos: {e}")
        raise


def get_extraction_summary(df):
    """
    Genera un resumen de los datos extraídos.
    
    Args:
        df (pd.DataFrame): DataFrame extraído
        
    Returns:
        dict: Diccionario con el resumen
    """
    summary = {
        'total_records': len(df),
        'total_columns': len(df.columns),
        'date_range': {
            'min': str(df['fecha'].min()),
            'max': str(df['fecha'].max())
        },
        'total_sales': float(df['total_venta'].sum()),
        'null_values': int(df.isnull().sum().sum()),
        'extraction_timestamp': datetime.now().isoformat()
    }
    
    logger.info("=" * 60)
    logger.info("RESUMEN DE EXTRACCIÓN")
    logger.info("=" * 60)
    logger.info(f"Total de registros: {summary['total_records']}")
    logger.info(f"Total de columnas: {summary['total_columns']}")
    logger.info(f"Rango de fechas: {summary['date_range']['min']} a {summary['date_range']['max']}")
    logger.info(f"Total de ventas: ${summary['total_sales']:,.2f}")
    logger.info(f"Valores nulos: {summary['null_values']}")
    logger.info("=" * 60)
    
    return summary


def extract(**kwargs):
    """
    Función principal de extracción para ser llamada por Airflow.
    
    Args:
        **kwargs: Argumentos de contexto de Airflow
        
    Returns:
        str: Ruta del archivo con datos extraídos
    """
    logger.info("=" * 60)
    logger.info("INICIANDO PROCESO DE EXTRACCIÓN (EXTRACT)")
    logger.info("=" * 60)
    
    try:
        # 1. Extraer datos de la base de datos
        df = extract_data_from_db()
        
        # 2. Validar datos extraídos
        if not validate_extracted_data(df):
            raise ValueError("Los datos extraídos no pasaron la validación")
        
        # 3. Guardar datos extraídos
        output_path = os.getenv('DATA_OUTPUT_PATH', 'data/output')
        filename = 'extracted_data.csv'
        save_extracted_data(df, output_path, filename)
        
        # 4. Generar resumen
        summary = get_extraction_summary(df)
        
        # 5. Retornar ruta del archivo (para XCom en Airflow)
        file_path = os.path.join(output_path, filename)
        
        logger.info("=" * 60)
        logger.info("✓ EXTRACCIÓN COMPLETADA EXITOSAMENTE")
        logger.info("=" * 60)
        
        return file_path
        
    except Exception as e:
        logger.error(f"❌ Error en el proceso de extracción: {e}")
        raise


if __name__ == "__main__":
    # Ejecutar extracción de forma independiente
    extract()
