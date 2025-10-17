"""
DAG de Apache Airflow para el proceso ETL de datos de ventas.

Este DAG orquesta el flujo completo de extracción, transformación y carga de datos:
1. Extract: Extrae datos desde la base de datos SQLite
2. Transform: Limpia, transforma y agrega los datos
3. Load: Carga los datos procesados en la tabla destino

Autor: Proyecto Educativo ETL
Fecha: 2025
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importar los scripts
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Importar las funciones ETL
from scripts.extract_data import extract
from scripts.transform_data import transform
from scripts.load_data import load

# ============================================================================
# CONFIGURACIÓN DEL DAG
# ============================================================================

# Argumentos por defecto para todas las tareas
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,  # No depende de ejecuciones anteriores
    'email': ['admin@example.com'],
    'email_on_failure': False,  # Cambiar a True para recibir emails en caso de fallo
    'email_on_retry': False,
    'retries': 2,  # Número de reintentos en caso de fallo
    'retry_delay': timedelta(minutes=5),  # Tiempo entre reintentos
    'execution_timeout': timedelta(minutes=30),  # Timeout máximo por tarea
}

# Descripción del DAG
dag_description = """
### Pipeline ETL de Datos de Ventas

Este DAG implementa un proceso ETL completo para procesar datos de ventas:

**Flujo de trabajo:**
1. **Extract**: Extrae datos desde la base de datos SQLite de origen
2. **Transform**: Limpia, valida y transforma los datos usando pandas
3. **Load**: Carga los datos procesados en la tabla destino

**Frecuencia**: Diaria a las 00:00 UTC

**Datos procesados**:
- Ventas por producto, categoría y región
- Agregaciones y métricas calculadas
- Limpieza de valores nulos y outliers

**Salidas**:
- Tabla `sales_transformed` en la base de datos
- Archivos CSV en `data/output/`
"""

# ============================================================================
# DEFINICIÓN DEL DAG
# ============================================================================

# Crear el DAG
dag = DAG(
    dag_id='etl_sales_pipeline',
    default_args=default_args,
    description='Pipeline ETL para procesar datos de ventas',
    doc_md=dag_description,
    schedule_interval='0 0 * * *',  # Ejecutar diariamente a medianoche (cron: min hour day month dayofweek)
    start_date=days_ago(1),  # Fecha de inicio (1 día atrás)
    catchup=False,  # No ejecutar para fechas pasadas
    tags=['etl', 'sales', 'data-pipeline', 'educational'],  # Tags para organización
    max_active_runs=1,  # Solo una ejecución activa a la vez
)

# ============================================================================
# DEFINICIÓN DE TAREAS
# ============================================================================

# Tarea 1: Inicio del pipeline (documentación)
start_task = BashOperator(
    task_id='start_pipeline',
    bash_command='echo "Iniciando pipeline ETL de ventas - $(date)"',
    dag=dag,
)

# Tarea 2: Extracción de datos
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract,
    provide_context=True,  # Proporciona contexto de Airflow a la función
    dag=dag,
    doc_md="""
    ### Tarea de Extracción
    
    Extrae datos desde la tabla `sales_data` en la base de datos SQLite.
    
    **Acciones**:
    - Conecta a la base de datos
    - Ejecuta query SELECT para extraer todos los registros
    - Valida los datos extraídos
    - Guarda los datos en `data/output/extracted_data.csv`
    
    **Salida**: Archivo CSV con datos extraídos
    """,
)

# Tarea 3: Transformación de datos
transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform,
    provide_context=True,
    dag=dag,
    doc_md="""
    ### Tarea de Transformación
    
    Limpia, valida y transforma los datos extraídos.
    
    **Acciones**:
    - Carga datos desde `extracted_data.csv`
    - Limpia valores nulos y duplicados
    - Elimina outliers usando método IQR
    - Normaliza texto y formatos
    - Agrega datos por producto, categoría y región
    - Calcula métricas derivadas
    
    **Salida**: Archivo CSV con datos transformados
    """,
)

# Tarea 4: Carga de datos
load_task = PythonOperator(
    task_id='load_data',
    python_callable=load,
    provide_context=True,
    dag=dag,
    doc_md="""
    ### Tarea de Carga
    
    Carga los datos transformados en la base de datos destino.
    
    **Acciones**:
    - Carga datos desde `transformed_data.csv`
    - Valida datos antes de la carga
    - Crea backup de datos existentes (opcional)
    - Inserta datos en tabla `sales_transformed`
    - Crea índices para optimizar consultas
    - Genera estadísticas de carga
    
    **Salida**: Datos cargados en la base de datos
    """,
)

# Tarea 5: Finalización del pipeline
end_task = BashOperator(
    task_id='end_pipeline',
    bash_command='echo "Pipeline ETL completado exitosamente - $(date)"',
    dag=dag,
)

# Tarea 6: Generar reporte de ejecución (opcional)
def generate_execution_report(**kwargs):
    """
    Genera un reporte resumido de la ejecución del pipeline.
    """
    import logging
    from datetime import datetime
    
    logger = logging.getLogger(__name__)
    
    # Obtener información del contexto de Airflow
    ti = kwargs['ti']
    execution_date = kwargs['execution_date']
    
    # Intentar obtener información de las tareas anteriores usando XCom
    try:
        extract_output = ti.xcom_pull(task_ids='extract_data')
        transform_output = ti.xcom_pull(task_ids='transform_data')
        load_output = ti.xcom_pull(task_ids='load_data')
        
        logger.info("=" * 60)
        logger.info("REPORTE DE EJECUCIÓN DEL PIPELINE ETL")
        logger.info("=" * 60)
        logger.info(f"Fecha de ejecución: {execution_date}")
        logger.info(f"Hora de finalización: {datetime.now()}")
        logger.info(f"\nArchivos generados:")
        logger.info(f"  - Extract: {extract_output}")
        logger.info(f"  - Transform: {transform_output}")
        logger.info(f"\nEstadísticas de carga:")
        if isinstance(load_output, dict):
            logger.info(f"  - Registros cargados: {load_output.get('total_records', 'N/A')}")
            logger.info(f"  - Total de ventas: ${load_output.get('total_sales', 0):,.2f}")
        logger.info("=" * 60)
        logger.info("✓ Pipeline ejecutado exitosamente")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.warning(f"No se pudo generar reporte completo: {e}")
        logger.info("Pipeline completado (reporte parcial)")

report_task = PythonOperator(
    task_id='generate_report',
    python_callable=generate_execution_report,
    provide_context=True,
    dag=dag,
)

# ============================================================================
# DEFINICIÓN DE DEPENDENCIAS (FLUJO DEL PIPELINE)
# ============================================================================

# Definir el orden de ejecución de las tareas
# Sintaxis: tarea_anterior >> tarea_siguiente

# Opción 1: Sintaxis encadenada (más legible)
start_task >> extract_task >> transform_task >> load_task >> report_task >> end_task

# Opción 2: Sintaxis alternativa (equivalente)
# start_task.set_downstream(extract_task)
# extract_task.set_downstream(transform_task)
# transform_task.set_downstream(load_task)
# load_task.set_downstream(report_task)
# report_task.set_downstream(end_task)

# Opción 3: Usando listas (para dependencias múltiples)
# [start_task] >> extract_task >> transform_task >> load_task >> [report_task, end_task]

# ============================================================================
# DOCUMENTACIÓN ADICIONAL
# ============================================================================

"""
NOTAS IMPORTANTES:

1. **Configuración de Airflow**:
   - Asegúrate de que AIRFLOW_HOME apunte al directorio correcto
   - El directorio 'dags' debe estar en AIRFLOW__CORE__DAGS_FOLDER
   - Ejecuta `airflow db init` antes de usar este DAG

2. **Variables de entorno**:
   - Configura el archivo .env con las rutas correctas
   - Las rutas deben ser absolutas para evitar problemas

3. **Dependencias**:
   - Instala todas las dependencias de requirements.txt
   - Verifica que pandas, sqlite3 y airflow estén instalados

4. **Ejecución**:
   - Inicia el scheduler: `airflow scheduler`
   - Inicia el webserver: `airflow webserver`
   - Accede a la UI en http://localhost:8080

5. **Monitoreo**:
   - Revisa los logs en la UI de Airflow
   - Los archivos de log están en airflow/logs/

6. **Testing**:
   - Prueba el DAG: `airflow dags test etl_sales_pipeline`
   - Prueba una tarea: `airflow tasks test etl_sales_pipeline extract_data 2025-01-01`

7. **Troubleshooting**:
   - Si las tareas fallan, revisa los logs en la UI
   - Verifica que la base de datos exista (ejecuta create_dummy_db.py)
   - Asegúrate de que los directorios data/input y data/output existan
"""
