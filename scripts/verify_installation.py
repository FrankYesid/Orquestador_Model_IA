"""
Script para verificar que la instalación del proyecto sea correcta.
Verifica dependencias, archivos, configuración y conectividad.
"""

import sys
import os
from pathlib import Path
import importlib
import sqlite3
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_header(title):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def check_python_version():
    """Verifica la versión de Python."""
    print_header("VERIFICANDO VERSIÓN DE PYTHON")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 11:
        logger.info(f"✓ Python {version_str} (Compatible)")
        return True
    else:
        logger.error(f"❌ Python {version_str} (Se requiere 3.11+)")
        return False


def check_dependencies():
    """Verifica que todas las dependencias estén instaladas."""
    print_header("VERIFICANDO DEPENDENCIAS")
    
    required_packages = {
        'airflow': 'apache-airflow',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'sqlalchemy': 'SQLAlchemy',
        'dotenv': 'python-dotenv',
    }
    
    all_installed = True
    
    for module_name, package_name in required_packages.items():
        try:
            importlib.import_module(module_name)
            logger.info(f"✓ {package_name}")
        except ImportError:
            logger.error(f"❌ {package_name} no instalado")
            all_installed = False
    
    return all_installed


def check_project_structure():
    """Verifica que la estructura del proyecto sea correcta."""
    print_header("VERIFICANDO ESTRUCTURA DEL PROYECTO")
    
    required_dirs = [
        'dags',
        'scripts',
        'config',
        'data/input',
        'data/output',
        'docker',
    ]
    
    required_files = [
        'requirements.txt',
        '.env',
        'README.md',
        'dags/etl_pipeline.py',
        'scripts/extract_data.py',
        'scripts/transform_data.py',
        'scripts/load_data.py',
        'scripts/create_dummy_db.py',
        'config/db_config.py',
    ]
    
    all_exist = True
    
    # Verificar directorios
    for directory in required_dirs:
        path = Path(directory)
        if path.exists() and path.is_dir():
            logger.info(f"✓ Directorio: {directory}")
        else:
            logger.error(f"❌ Directorio faltante: {directory}")
            all_exist = False
    
    # Verificar archivos
    for file in required_files:
        path = Path(file)
        if path.exists() and path.is_file():
            logger.info(f"✓ Archivo: {file}")
        else:
            logger.error(f"❌ Archivo faltante: {file}")
            all_exist = False
    
    return all_exist


def check_environment_variables():
    """Verifica que las variables de entorno estén configuradas."""
    print_header("VERIFICANDO VARIABLES DE ENTORNO")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'PROJECT_ROOT',
        'DATA_INPUT_PATH',
        'DATA_OUTPUT_PATH',
        'DB_PATH',
        'AIRFLOW__CORE__DAGS_FOLDER',
    ]
    
    all_set = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"✓ {var}: {value}")
        else:
            logger.warning(f"⚠ {var} no configurada")
            all_set = False
    
    return all_set


def check_database():
    """Verifica que la base de datos exista y tenga datos."""
    print_header("VERIFICANDO BASE DE DATOS")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    db_path = os.getenv('DB_PATH', 'data/database.db')
    
    if not Path(db_path).exists():
        logger.error(f"❌ Base de datos no encontrada: {db_path}")
        logger.info("   Ejecuta: python scripts/create_dummy_db.py")
        return False
    
    logger.info(f"✓ Base de datos encontrada: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tabla de origen
        cursor.execute("SELECT COUNT(*) FROM sales_data")
        count = cursor.fetchone()[0]
        logger.info(f"✓ Tabla 'sales_data': {count} registros")
        
        # Verificar tabla de destino
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales_transformed'")
        if cursor.fetchone():
            cursor.execute("SELECT COUNT(*) FROM sales_transformed")
            count = cursor.fetchone()[0]
            logger.info(f"✓ Tabla 'sales_transformed': {count} registros")
        else:
            logger.info("ℹ Tabla 'sales_transformed' vacía (se llenará al ejecutar el pipeline)")
        
        conn.close()
        return True
    except Exception as e:
        logger.error(f"❌ Error verificando base de datos: {e}")
        return False


def check_airflow_installation():
    """Verifica que Airflow esté instalado y configurado."""
    print_header("VERIFICANDO AIRFLOW")
    
    try:
        import airflow
        logger.info(f"✓ Airflow versión: {airflow.__version__}")
        
        # Verificar AIRFLOW_HOME
        airflow_home = os.getenv('AIRFLOW_HOME')
        if airflow_home:
            logger.info(f"✓ AIRFLOW_HOME: {airflow_home}")
            
            # Verificar base de datos de Airflow
            airflow_db = Path(airflow_home) / 'airflow.db'
            if airflow_db.exists():
                logger.info(f"✓ Base de datos de Airflow inicializada")
            else:
                logger.warning(f"⚠ Base de datos de Airflow no inicializada")
                logger.info("   Ejecuta: airflow db init")
                return False
        else:
            logger.warning("⚠ AIRFLOW_HOME no configurada")
            return False
        
        return True
    except ImportError:
        logger.error("❌ Airflow no instalado")
        return False


def check_dag_validity():
    """Verifica que el DAG sea válido."""
    print_header("VERIFICANDO DAG")
    
    try:
        # Importar el DAG
        sys.path.insert(0, str(Path.cwd()))
        from dags.etl_pipeline import dag
        
        logger.info(f"✓ DAG importado: {dag.dag_id}")
        logger.info(f"✓ Número de tareas: {len(dag.tasks)}")
        logger.info(f"✓ Schedule: {dag.schedule_interval}")
        
        # Listar tareas
        logger.info("\nTareas del DAG:")
        for task in dag.tasks:
            logger.info(f"  - {task.task_id}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Error importando DAG: {e}")
        return False


def print_summary(results):
    """Imprime un resumen de la verificación."""
    print_header("RESUMEN DE VERIFICACIÓN")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"\nTotal de verificaciones: {total}")
    print(f"✓ Pasadas: {passed}")
    print(f"❌ Fallidas: {failed}")
    
    if failed == 0:
        print("\n🎉 ¡Todas las verificaciones pasaron!")
        print("El proyecto está listo para usar.")
        print("\nPara iniciar Airflow:")
        print("  Terminal 1: airflow scheduler")
        print("  Terminal 2: airflow webserver --port 8080")
    else:
        print("\n⚠ Algunas verificaciones fallaron.")
        print("Por favor, revisa los errores arriba y corrígelos.")
        print("\nPara más ayuda, consulta:")
        print("  - README.md")
        print("  - QUICKSTART.md")


def main():
    """Función principal que ejecuta todas las verificaciones."""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🔍 VERIFICACIÓN DE INSTALACIÓN                         ║
    ║   Proyecto ETL con Apache Airflow                        ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    checks = {
        'Python Version': check_python_version,
        'Dependencies': check_dependencies,
        'Project Structure': check_project_structure,
        'Environment Variables': check_environment_variables,
        'Database': check_database,
        'Airflow Installation': check_airflow_installation,
        'DAG Validity': check_dag_validity,
    }
    
    results = {}
    
    for check_name, check_func in checks.items():
        try:
            results[check_name] = check_func()
        except Exception as e:
            logger.error(f"❌ Error en verificación '{check_name}': {e}")
            results[check_name] = False
    
    print_summary(results)
    
    # Retornar código de salida
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
