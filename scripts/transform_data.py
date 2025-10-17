"""
Script de Transformación (Transform) del proceso ETL.
Limpia, transforma y agrega los datos extraídos.
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import logging

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()


def load_extracted_data(file_path=None):
    """
    Carga los datos extraídos desde un archivo CSV.
    
    Args:
        file_path (str, optional): Ruta del archivo a cargar
        
    Returns:
        pd.DataFrame: DataFrame con los datos cargados
    """
    if file_path is None:
        output_path = os.getenv('DATA_OUTPUT_PATH', 'data/output')
        file_path = os.path.join(output_path, 'extracted_data.csv')
    
    logger.info(f"Cargando datos desde: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        logger.info(f"✓ Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
        return df
    except Exception as e:
        logger.error(f"Error cargando datos: {e}")
        raise


def clean_data(df):
    """
    Limpia los datos: maneja valores nulos, duplicados y outliers.
    
    Args:
        df (pd.DataFrame): DataFrame a limpiar
        
    Returns:
        pd.DataFrame: DataFrame limpio
    """
    logger.info("Iniciando limpieza de datos...")
    
    df_clean = df.copy()
    initial_rows = len(df_clean)
    
    # 1. Convertir fecha a datetime
    df_clean['fecha'] = pd.to_datetime(df_clean['fecha'])
    logger.info("✓ Fechas convertidas a datetime")
    
    # 2. Eliminar duplicados completos
    duplicates = df_clean.duplicated().sum()
    if duplicates > 0:
        df_clean = df_clean.drop_duplicates()
        logger.info(f"✓ Eliminados {duplicates} registros duplicados")
    
    # 3. Manejar valores nulos
    # Rellenar descuentos nulos con 0
    if 'descuento' in df_clean.columns:
        null_discounts = df_clean['descuento'].isnull().sum()
        if null_discounts > 0:
            df_clean['descuento'] = df_clean['descuento'].fillna(0)
            logger.info(f"✓ Rellenados {null_discounts} valores nulos en 'descuento' con 0")
    
    # Eliminar filas con valores nulos en columnas críticas
    critical_columns = ['fecha', 'producto', 'cantidad', 'precio_unitario']
    null_critical = df_clean[critical_columns].isnull().any(axis=1).sum()
    if null_critical > 0:
        df_clean = df_clean.dropna(subset=critical_columns)
        logger.info(f"✓ Eliminadas {null_critical} filas con valores nulos en columnas críticas")
    
    # 4. Validar y limpiar valores numéricos
    # Eliminar cantidades negativas o cero
    invalid_qty = (df_clean['cantidad'] <= 0).sum()
    if invalid_qty > 0:
        df_clean = df_clean[df_clean['cantidad'] > 0]
        logger.info(f"✓ Eliminadas {invalid_qty} filas con cantidad <= 0")
    
    # Eliminar precios negativos o cero
    invalid_price = (df_clean['precio_unitario'] <= 0).sum()
    if invalid_price > 0:
        df_clean = df_clean[df_clean['precio_unitario'] > 0]
        logger.info(f"✓ Eliminadas {invalid_price} filas con precio <= 0")
    
    # 5. Detectar y manejar outliers usando IQR
    def remove_outliers(df, column):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 3 * IQR
        upper_bound = Q3 + 3 * IQR
        
        outliers = ((df[column] < lower_bound) | (df[column] > upper_bound)).sum()
        df_filtered = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
        
        return df_filtered, outliers
    
    # Remover outliers en total_venta
    if 'total_venta' in df_clean.columns:
        df_clean, outliers_removed = remove_outliers(df_clean, 'total_venta')
        if outliers_removed > 0:
            logger.info(f"✓ Eliminados {outliers_removed} outliers en 'total_venta'")
    
    # 6. Normalizar texto
    text_columns = ['producto', 'categoria', 'region']
    for col in text_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].str.strip().str.title()
    logger.info("✓ Texto normalizado en columnas de categoría")
    
    final_rows = len(df_clean)
    rows_removed = initial_rows - final_rows
    
    logger.info("=" * 60)
    logger.info(f"✓ Limpieza completada")
    logger.info(f"  Filas iniciales: {initial_rows}")
    logger.info(f"  Filas finales: {final_rows}")
    logger.info(f"  Filas eliminadas: {rows_removed} ({rows_removed/initial_rows*100:.2f}%)")
    logger.info("=" * 60)
    
    return df_clean


def transform_data(df):
    """
    Transforma los datos: crea nuevas columnas y agrega información.
    
    Args:
        df (pd.DataFrame): DataFrame a transformar
        
    Returns:
        pd.DataFrame: DataFrame transformado
    """
    logger.info("Iniciando transformación de datos...")
    
    df_transformed = df.copy()
    
    # 1. Extraer componentes de fecha
    df_transformed['año'] = df_transformed['fecha'].dt.year
    df_transformed['mes'] = df_transformed['fecha'].dt.month
    df_transformed['dia'] = df_transformed['fecha'].dt.day
    df_transformed['dia_semana'] = df_transformed['fecha'].dt.dayofweek
    df_transformed['nombre_dia'] = df_transformed['fecha'].dt.day_name()
    df_transformed['trimestre'] = df_transformed['fecha'].dt.quarter
    logger.info("✓ Componentes de fecha extraídos")
    
    # 2. Calcular métricas derivadas
    df_transformed['ingreso_bruto'] = df_transformed['cantidad'] * df_transformed['precio_unitario']
    df_transformed['descuento_total'] = df_transformed['ingreso_bruto'] * df_transformed['descuento']
    df_transformed['margen'] = df_transformed['total_venta'] - (df_transformed['ingreso_bruto'] * 0.6)  # Asumiendo 40% de margen
    logger.info("✓ Métricas derivadas calculadas")
    
    # 3. Categorizar ventas
    def categorize_sale(total):
        if total < 100:
            return 'Pequeña'
        elif total < 500:
            return 'Mediana'
        elif total < 1000:
            return 'Grande'
        else:
            return 'Premium'
    
    df_transformed['categoria_venta'] = df_transformed['total_venta'].apply(categorize_sale)
    logger.info("✓ Ventas categorizadas")
    
    # 4. Crear flags booleanos
    df_transformed['tiene_descuento'] = df_transformed['descuento'] > 0
    df_transformed['venta_alta'] = df_transformed['total_venta'] > df_transformed['total_venta'].median()
    logger.info("✓ Flags booleanos creados")
    
    logger.info(f"✓ Transformación completada: {df_transformed.shape[1]} columnas totales")
    
    return df_transformed


def aggregate_data(df):
    """
    Agrega los datos por producto, categoría y región.
    
    Args:
        df (pd.DataFrame): DataFrame a agregar
        
    Returns:
        pd.DataFrame: DataFrame agregado
    """
    logger.info("Iniciando agregación de datos...")
    
    # Agregar por producto, categoría y región
    df_aggregated = df.groupby(['fecha', 'producto', 'categoria', 'region']).agg({
        'cantidad': 'sum',
        'precio_unitario': 'mean',
        'descuento': 'mean',
        'total_venta': 'sum',
        'id': 'count'  # Número de transacciones
    }).reset_index()
    
    # Renombrar columnas
    df_aggregated.rename(columns={
        'cantidad': 'cantidad_total',
        'precio_unitario': 'precio_promedio',
        'descuento': 'descuento_promedio',
        'id': 'num_transacciones'
    }, inplace=True)
    
    # Redondear valores
    df_aggregated['precio_promedio'] = df_aggregated['precio_promedio'].round(2)
    df_aggregated['descuento_promedio'] = df_aggregated['descuento_promedio'].round(4)
    df_aggregated['total_venta'] = df_aggregated['total_venta'].round(2)
    
    logger.info(f"✓ Datos agregados: {len(df)} filas → {len(df_aggregated)} filas")
    logger.info(f"  Reducción: {(1 - len(df_aggregated)/len(df))*100:.2f}%")
    
    return df_aggregated


def save_transformed_data(df, output_path=None, filename='transformed_data.csv'):
    """
    Guarda los datos transformados en un archivo CSV.
    
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
        logger.info(f"✓ Datos transformados guardados en: {file_path}")
        logger.info(f"  Tamaño del archivo: {os.path.getsize(file_path) / 1024:.2f} KB")
    except Exception as e:
        logger.error(f"Error guardando datos: {e}")
        raise


def get_transformation_summary(df_original, df_transformed):
    """
    Genera un resumen de la transformación.
    
    Args:
        df_original (pd.DataFrame): DataFrame original
        df_transformed (pd.DataFrame): DataFrame transformado
        
    Returns:
        dict: Diccionario con el resumen
    """
    summary = {
        'original_records': len(df_original),
        'transformed_records': len(df_transformed),
        'reduction_percentage': ((len(df_original) - len(df_transformed)) / len(df_original) * 100),
        'original_columns': len(df_original.columns),
        'transformed_columns': len(df_transformed.columns),
        'total_sales': float(df_transformed['total_venta'].sum()),
        'transformation_timestamp': datetime.now().isoformat()
    }
    
    logger.info("=" * 60)
    logger.info("RESUMEN DE TRANSFORMACIÓN")
    logger.info("=" * 60)
    logger.info(f"Registros originales: {summary['original_records']}")
    logger.info(f"Registros transformados: {summary['transformed_records']}")
    logger.info(f"Reducción: {summary['reduction_percentage']:.2f}%")
    logger.info(f"Columnas originales: {summary['original_columns']}")
    logger.info(f"Columnas transformadas: {summary['transformed_columns']}")
    logger.info(f"Total de ventas: ${summary['total_sales']:,.2f}")
    logger.info("=" * 60)
    
    return summary


def transform(**kwargs):
    """
    Función principal de transformación para ser llamada por Airflow.
    
    Args:
        **kwargs: Argumentos de contexto de Airflow
        
    Returns:
        str: Ruta del archivo con datos transformados
    """
    logger.info("=" * 60)
    logger.info("INICIANDO PROCESO DE TRANSFORMACIÓN (TRANSFORM)")
    logger.info("=" * 60)
    
    try:
        # 1. Cargar datos extraídos
        df_original = load_extracted_data()
        
        # 2. Limpiar datos
        df_clean = clean_data(df_original)
        
        # 3. Transformar datos
        df_transformed_full = transform_data(df_clean)
        
        # 4. Agregar datos
        df_aggregated = aggregate_data(df_clean)
        
        # 5. Guardar datos transformados
        output_path = os.getenv('DATA_OUTPUT_PATH', 'data/output')
        save_transformed_data(df_aggregated, output_path, 'transformed_data.csv')
        
        # También guardar versión completa (sin agregar)
        save_transformed_data(df_transformed_full, output_path, 'transformed_data_full.csv')
        
        # 6. Generar resumen
        summary = get_transformation_summary(df_original, df_aggregated)
        
        # 7. Retornar ruta del archivo (para XCom en Airflow)
        file_path = os.path.join(output_path, 'transformed_data.csv')
        
        logger.info("=" * 60)
        logger.info("✓ TRANSFORMACIÓN COMPLETADA EXITOSAMENTE")
        logger.info("=" * 60)
        
        return file_path
        
    except Exception as e:
        logger.error(f"❌ Error en el proceso de transformación: {e}")
        raise


if __name__ == "__main__":
    # Ejecutar transformación de forma independiente
    transform()
