"""
Script de Carga (Load) del proceso ETL.
Carga los datos transformados en la tabla destino de la base de datos.
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


def load_transformed_data(file_path=None):
    """
    Carga los datos transformados desde un archivo CSV.
    
    Args:
        file_path (str, optional): Ruta del archivo a cargar
        
    Returns:
        pd.DataFrame: DataFrame con los datos cargados
    """
    if file_path is None:
        output_path = os.getenv('DATA_OUTPUT_PATH', 'data/output')
        file_path = os.path.join(output_path, 'transformed_data.csv')
    
    logger.info(f"Cargando datos transformados desde: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        logger.info(f"✓ Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
        return df
    except Exception as e:
        logger.error(f"Error cargando datos: {e}")
        raise


def validate_data_before_load(df):
    """
    Valida los datos antes de cargarlos en la base de datos.
    
    Args:
        df (pd.DataFrame): DataFrame a validar
        
    Returns:
        bool: True si los datos son válidos
    """
    logger.info("Validando datos antes de la carga...")
    
    validations = []
    
    # 1. Verificar que no esté vacío
    if df.empty:
        logger.error("❌ El DataFrame está vacío")
        return False
    else:
        logger.info(f"✓ DataFrame contiene {len(df)} registros")
        validations.append(True)
    
    # 2. Verificar columnas requeridas
    required_columns = ['fecha', 'producto', 'categoria', 'region', 
                       'cantidad_total', 'precio_promedio', 'total_venta', 'num_transacciones']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        logger.error(f"❌ Columnas faltantes: {missing_columns}")
        validations.append(False)
    else:
        logger.info("✓ Todas las columnas requeridas están presentes")
        validations.append(True)
    
    # 3. Verificar valores nulos en columnas críticas
    critical_columns = ['fecha', 'producto', 'total_venta']
    null_counts = df[critical_columns].isnull().sum()
    
    if null_counts.sum() > 0:
        logger.error(f"❌ Valores nulos en columnas críticas: {null_counts[null_counts > 0].to_dict()}")
        validations.append(False)
    else:
        logger.info("✓ No hay valores nulos en columnas críticas")
        validations.append(True)
    
    # 4. Verificar valores numéricos válidos
    numeric_columns = ['cantidad_total', 'precio_promedio', 'total_venta', 'num_transacciones']
    for col in numeric_columns:
        if col in df.columns:
            if (df[col] < 0).any():
                logger.error(f"❌ Valores negativos encontrados en '{col}'")
                validations.append(False)
            else:
                validations.append(True)
    
    # 5. Verificar duplicados
    duplicates = df.duplicated(subset=['fecha', 'producto', 'categoria', 'region']).sum()
    if duplicates > 0:
        logger.warning(f"⚠ Se encontraron {duplicates} registros duplicados")
        # No es crítico, pero se reporta
    
    # Resultado final
    is_valid = all(validations)
    if is_valid:
        logger.info("✓ Validación completada exitosamente")
    else:
        logger.error("❌ Validación falló")
    
    return is_valid


def prepare_data_for_load(df):
    """
    Prepara los datos para la carga en la base de datos.
    
    Args:
        df (pd.DataFrame): DataFrame a preparar
        
    Returns:
        pd.DataFrame: DataFrame preparado
    """
    logger.info("Preparando datos para la carga...")
    
    df_prepared = df.copy()
    
    # 1. Convertir fecha a string para SQLite
    if 'fecha' in df_prepared.columns:
        df_prepared['fecha'] = pd.to_datetime(df_prepared['fecha']).dt.strftime('%Y-%m-%d')
        logger.info("✓ Fechas convertidas a formato string")
    
    # 2. Asegurar tipos de datos correctos
    numeric_columns = ['cantidad_total', 'precio_promedio', 'descuento_promedio', 
                      'total_venta', 'num_transacciones']
    
    for col in numeric_columns:
        if col in df_prepared.columns:
            df_prepared[col] = pd.to_numeric(df_prepared[col], errors='coerce')
    
    logger.info("✓ Tipos de datos verificados")
    
    # 3. Eliminar columnas innecesarias si existen
    columns_to_drop = ['Unnamed: 0', 'index']
    df_prepared = df_prepared.drop(columns=[col for col in columns_to_drop if col in df_prepared.columns])
    
    # 4. Ordenar por fecha
    df_prepared = df_prepared.sort_values('fecha')
    logger.info("✓ Datos ordenados por fecha")
    
    logger.info(f"✓ Datos preparados: {df_prepared.shape}")
    
    return df_prepared


def load_to_database(df, table_name=None, if_exists='replace'):
    """
    Carga los datos en la base de datos SQLite.
    
    Args:
        df (pd.DataFrame): DataFrame a cargar
        table_name (str, optional): Nombre de la tabla destino
        if_exists (str): Acción si la tabla existe ('replace', 'append', 'fail')
        
    Returns:
        int: Número de registros cargados
    """
    if table_name is None:
        table_name = db_config.table_target
    
    logger.info(f"Cargando datos en la tabla: {table_name}")
    logger.info(f"Modo de carga: {if_exists}")
    
    conn = db_config.get_connection()
    
    try:
        # Cargar datos
        df.to_sql(
            table_name,
            conn,
            if_exists=if_exists,
            index=False
        )
        
        records_loaded = len(df)
        logger.info(f"✓ {records_loaded} registros cargados exitosamente")
        
        # Verificar la carga
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_records = cursor.fetchone()[0]
        logger.info(f"✓ Total de registros en la tabla: {total_records}")
        
        cursor.close()
        
        return records_loaded
        
    except Exception as e:
        logger.error(f"Error cargando datos: {e}")
        raise
    finally:
        db_config.close_connection(conn)


def create_indexes(table_name=None):
    """
    Crea índices en la tabla para mejorar el rendimiento de consultas.
    
    Args:
        table_name (str, optional): Nombre de la tabla
    """
    if table_name is None:
        table_name = db_config.table_target
    
    logger.info(f"Creando índices en la tabla: {table_name}")
    
    indexes = [
        f"CREATE INDEX IF NOT EXISTS idx_{table_name}_fecha ON {table_name}(fecha)",
        f"CREATE INDEX IF NOT EXISTS idx_{table_name}_producto ON {table_name}(producto)",
        f"CREATE INDEX IF NOT EXISTS idx_{table_name}_categoria ON {table_name}(categoria)",
        f"CREATE INDEX IF NOT EXISTS idx_{table_name}_region ON {table_name}(region)"
    ]
    
    try:
        for index_query in indexes:
            db_config.execute_query(index_query)
        
        logger.info(f"✓ {len(indexes)} índices creados exitosamente")
    except Exception as e:
        logger.error(f"Error creando índices: {e}")
        # No es crítico, continuar


def generate_load_statistics(table_name=None):
    """
    Genera estadísticas sobre los datos cargados.
    
    Args:
        table_name (str, optional): Nombre de la tabla
        
    Returns:
        dict: Diccionario con las estadísticas
    """
    if table_name is None:
        table_name = db_config.table_target
    
    logger.info("Generando estadísticas de carga...")
    
    conn = db_config.get_connection()
    
    try:
        # Total de registros
        query_count = f"SELECT COUNT(*) FROM {table_name}"
        total_records = pd.read_sql_query(query_count, conn).iloc[0, 0]
        
        # Total de ventas
        query_sales = f"SELECT SUM(total_venta) as total FROM {table_name}"
        total_sales = pd.read_sql_query(query_sales, conn).iloc[0, 0]
        
        # Rango de fechas
        query_dates = f"SELECT MIN(fecha) as min_date, MAX(fecha) as max_date FROM {table_name}"
        dates = pd.read_sql_query(query_dates, conn)
        
        # Top productos
        query_top_products = f"""
            SELECT producto, SUM(total_venta) as total
            FROM {table_name}
            GROUP BY producto
            ORDER BY total DESC
            LIMIT 5
        """
        top_products = pd.read_sql_query(query_top_products, conn)
        
        # Top regiones
        query_top_regions = f"""
            SELECT region, SUM(total_venta) as total
            FROM {table_name}
            GROUP BY region
            ORDER BY total DESC
            LIMIT 5
        """
        top_regions = pd.read_sql_query(query_top_regions, conn)
        
        statistics = {
            'total_records': int(total_records),
            'total_sales': float(total_sales) if total_sales else 0,
            'date_range': {
                'min': str(dates.iloc[0, 0]),
                'max': str(dates.iloc[0, 1])
            },
            'top_products': top_products.to_dict('records'),
            'top_regions': top_regions.to_dict('records'),
            'load_timestamp': datetime.now().isoformat()
        }
        
        logger.info("=" * 60)
        logger.info("ESTADÍSTICAS DE CARGA")
        logger.info("=" * 60)
        logger.info(f"Total de registros: {statistics['total_records']}")
        logger.info(f"Total de ventas: ${statistics['total_sales']:,.2f}")
        logger.info(f"Rango de fechas: {statistics['date_range']['min']} a {statistics['date_range']['max']}")
        logger.info("\nTop 5 Productos:")
        for i, prod in enumerate(statistics['top_products'], 1):
            logger.info(f"  {i}. {prod['producto']}: ${prod['total']:,.2f}")
        logger.info("\nTop 5 Regiones:")
        for i, reg in enumerate(statistics['top_regions'], 1):
            logger.info(f"  {i}. {reg['region']}: ${reg['total']:,.2f}")
        logger.info("=" * 60)
        
        return statistics
        
    except Exception as e:
        logger.error(f"Error generando estadísticas: {e}")
        raise
    finally:
        db_config.close_connection(conn)


def backup_existing_data(table_name=None):
    """
    Crea un backup de los datos existentes antes de cargar nuevos datos.
    
    Args:
        table_name (str, optional): Nombre de la tabla
    """
    if table_name is None:
        table_name = db_config.table_target
    
    # Verificar si la tabla existe
    if not db_config.table_exists(table_name):
        logger.info(f"La tabla {table_name} no existe, no se requiere backup")
        return
    
    backup_table = f"{table_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    logger.info(f"Creando backup de {table_name} como {backup_table}")
    
    query = f"CREATE TABLE {backup_table} AS SELECT * FROM {table_name}"
    
    try:
        db_config.execute_query(query)
        logger.info(f"✓ Backup creado exitosamente: {backup_table}")
    except Exception as e:
        logger.warning(f"⚠ No se pudo crear backup: {e}")
        # No es crítico, continuar


def load(**kwargs):
    """
    Función principal de carga para ser llamada por Airflow.
    
    Args:
        **kwargs: Argumentos de contexto de Airflow
        
    Returns:
        dict: Estadísticas de la carga
    """
    logger.info("=" * 60)
    logger.info("INICIANDO PROCESO DE CARGA (LOAD)")
    logger.info("=" * 60)
    
    try:
        # 1. Cargar datos transformados
        df = load_transformed_data()
        
        # 2. Validar datos
        if not validate_data_before_load(df):
            raise ValueError("Los datos no pasaron la validación")
        
        # 3. Preparar datos
        df_prepared = prepare_data_for_load(df)
        
        # 4. Crear backup (opcional)
        backup_existing_data()
        
        # 5. Cargar datos en la base de datos
        records_loaded = load_to_database(df_prepared, if_exists='replace')
        
        # 6. Crear índices
        create_indexes()
        
        # 7. Generar estadísticas
        statistics = generate_load_statistics()
        
        logger.info("=" * 60)
        logger.info("✓ CARGA COMPLETADA EXITOSAMENTE")
        logger.info(f"✓ {records_loaded} registros cargados")
        logger.info("=" * 60)
        
        return statistics
        
    except Exception as e:
        logger.error(f"❌ Error en el proceso de carga: {e}")
        raise


if __name__ == "__main__":
    # Ejecutar carga de forma independiente
    load()
