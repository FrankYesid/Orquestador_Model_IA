"""
Script de configuración automática del proyecto.
Ejecuta todos los pasos necesarios para inicializar el proyecto.
"""

import os
import sys
import subprocess
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_banner():
    """Imprime el banner del proyecto."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🚀 PROYECTO ETL CON APACHE AIRFLOW                     ║
    ║   Script de Configuración Automática                     ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_python_version():
    """Verifica que la versión de Python sea compatible."""
    logger.info("Verificando versión de Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        logger.error(f"❌ Python 3.11+ requerido. Versión actual: {version.major}.{version.minor}")
        return False
    
    logger.info(f"✓ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True


def create_directories():
    """Crea los directorios necesarios del proyecto."""
    logger.info("Creando directorios del proyecto...")
    
    directories = [
        'data/input',
        'data/output',
        'airflow/logs',
        'airflow/plugins',
        'logs'
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"✓ Directorio creado: {directory}")
    
    return True


def install_dependencies():
    """Instala las dependencias del proyecto."""
    logger.info("Instalando dependencias...")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            check=True,
            capture_output=True
        )
        logger.info("✓ pip actualizado")
        
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True
        )
        logger.info("✓ Dependencias instaladas")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error instalando dependencias: {e}")
        return False


def setup_environment():
    """Configura las variables de entorno."""
    logger.info("Configurando variables de entorno...")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        # Copiar .env.example a .env
        import shutil
        shutil.copy(env_example, env_file)
        logger.info("✓ Archivo .env creado desde .env.example")
        logger.warning("⚠ Por favor, edita .env con las rutas correctas de tu sistema")
    elif env_file.exists():
        logger.info("✓ Archivo .env ya existe")
    else:
        logger.warning("⚠ No se encontró .env.example")
    
    return True


def create_dummy_database():
    """Crea la base de datos dummy con datos de ejemplo."""
    logger.info("Creando base de datos dummy...")
    
    try:
        # Importar y ejecutar el script de creación
        from scripts.create_dummy_db import main
        main()
        logger.info("✓ Base de datos dummy creada")
        return True
    except Exception as e:
        logger.error(f"❌ Error creando base de datos: {e}")
        return False


def initialize_airflow():
    """Inicializa la base de datos de Airflow."""
    logger.info("Inicializando Airflow...")
    
    # Establecer AIRFLOW_HOME
    airflow_home = Path.cwd() / 'airflow'
    os.environ['AIRFLOW_HOME'] = str(airflow_home)
    
    try:
        # Inicializar base de datos de Airflow
        subprocess.run(
            ["airflow", "db", "init"],
            check=True,
            capture_output=True,
            env=os.environ
        )
        logger.info("✓ Base de datos de Airflow inicializada")
        
        # Crear usuario admin
        subprocess.run(
            [
                "airflow", "users", "create",
                "--username", "admin",
                "--firstname", "Admin",
                "--lastname", "User",
                "--role", "Admin",
                "--email", "admin@example.com",
                "--password", "admin"
            ],
            check=True,
            capture_output=True,
            env=os.environ
        )
        logger.info("✓ Usuario admin creado (usuario: admin, contraseña: admin)")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error inicializando Airflow: {e}")
        return False
    except FileNotFoundError:
        logger.warning("⚠ Airflow no encontrado. Instala las dependencias primero.")
        return False


def print_next_steps():
    """Imprime los siguientes pasos para el usuario."""
    next_steps = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ✅ CONFIGURACIÓN COMPLETADA                            ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    
    📋 SIGUIENTES PASOS:
    
    1. Edita el archivo .env con las rutas correctas de tu sistema
    
    2. Inicia Airflow:
       
       Terminal 1 (Scheduler):
       $ airflow scheduler
       
       Terminal 2 (Webserver):
       $ airflow webserver --port 8080
    
    3. Accede a la interfaz web:
       URL: http://localhost:8080
       Usuario: admin
       Contraseña: admin
    
    4. Activa y ejecuta el DAG 'etl_sales_pipeline'
    
    📚 DOCUMENTACIÓN:
    - README.md: Documentación completa
    - QUICKSTART.md: Guía de inicio rápido
    - CONTRIBUTING.md: Guía de contribución
    
    ❓ ¿Necesitas ayuda?
    - Revisa el README.md
    - Abre un issue en GitHub
    
    ¡Disfruta del proyecto! 🚀
    """
    print(next_steps)


def main():
    """Función principal que ejecuta todos los pasos de configuración."""
    print_banner()
    
    steps = [
        ("Verificar Python", check_python_version),
        ("Crear directorios", create_directories),
        ("Configurar entorno", setup_environment),
        ("Instalar dependencias", install_dependencies),
        ("Crear base de datos", create_dummy_database),
        ("Inicializar Airflow", initialize_airflow),
    ]
    
    logger.info("Iniciando configuración del proyecto...")
    logger.info("=" * 60)
    
    for step_name, step_func in steps:
        logger.info(f"\n📌 Paso: {step_name}")
        logger.info("-" * 60)
        
        try:
            success = step_func()
            if not success:
                logger.error(f"❌ Falló el paso: {step_name}")
                logger.error("Configuración interrumpida. Por favor, revisa los errores.")
                return False
        except Exception as e:
            logger.error(f"❌ Error en {step_name}: {e}")
            return False
    
    logger.info("\n" + "=" * 60)
    print_next_steps()
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
