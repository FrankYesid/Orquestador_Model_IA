#!/usr/bin/env python
"""
Script de Inicio Rápido para el Proyecto ETL con Apache Airflow.
Automatiza todos los pasos necesarios para poner en marcha el proyecto.
"""

import os
import sys
import subprocess
import time
from pathlib import Path
import logging

# Configurar logging con colores
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


class Colors:
    """Códigos de color ANSI para terminal."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_banner():
    """Imprime el banner del proyecto."""
    banner = f"""
{Colors.BLUE}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🚀 PROYECTO ETL CON APACHE AIRFLOW                         ║
║   Script de Inicio Rápido                                    ║
║                                                               ║
║   Este script automatizará:                                  ║
║   ✓ Instalación de dependencias                              ║
║   ✓ Creación de base de datos dummy                          ║
║   ✓ Inicialización de Airflow                                ║
║   ✓ Creación de usuario admin                                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.END}
    """
    print(banner)


def print_step(step_number, total_steps, description):
    """Imprime el paso actual."""
    print(f"\n{Colors.BOLD}[{step_number}/{total_steps}] {description}{Colors.END}")
    print("─" * 60)


def print_success(message):
    """Imprime mensaje de éxito."""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_warning(message):
    """Imprime mensaje de advertencia."""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def print_error(message):
    """Imprime mensaje de error."""
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def check_python_version():
    """Verifica la versión de Python."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print_error(f"Python 3.11+ requerido. Versión actual: {version.major}.{version.minor}")
        return False
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detectado")
    return True


def run_command(command, description, check=True, shell=False):
    """Ejecuta un comando del sistema."""
    try:
        print(f"  Ejecutando: {description}...")
        result = subprocess.run(
            command,
            check=check,
            capture_output=True,
            text=True,
            shell=shell
        )
        print_success(description)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"{description} falló")
        if e.stderr:
            print(f"  Error: {e.stderr[:200]}")
        return False
    except Exception as e:
        print_error(f"{description} falló: {str(e)}")
        return False


def install_dependencies():
    """Instala las dependencias del proyecto."""
    print_step(1, 5, "Instalando Dependencias")
    
    # Actualizar pip
    if not run_command(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
        "Actualizar pip"
    ):
        return False
    
    # Instalar dependencias
    if not run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        "Instalar dependencias del proyecto"
    ):
        return False
    
    return True


def create_directories():
    """Crea los directorios necesarios."""
    print_step(2, 5, "Creando Directorios")
    
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
        print_success(f"Directorio: {directory}")
    
    return True


def setup_environment():
    """Configura las variables de entorno."""
    print_step(3, 5, "Configurando Variables de Entorno")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print_success("Archivo .env creado desde .env.example")
        print_warning("Edita .env con las rutas correctas de tu sistema")
    elif env_file.exists():
        print_success("Archivo .env ya existe")
    else:
        print_warning("No se encontró .env.example")
    
    return True


def create_database():
    """Crea la base de datos dummy."""
    print_step(4, 5, "Creando Base de Datos Dummy")
    
    if not run_command(
        [sys.executable, "scripts/create_dummy_db.py"],
        "Crear base de datos con datos de ejemplo"
    ):
        return False
    
    return True


def initialize_airflow():
    """Inicializa Airflow."""
    print_step(5, 5, "Inicializando Apache Airflow")
    
    # Establecer AIRFLOW_HOME
    airflow_home = Path.cwd() / 'airflow'
    os.environ['AIRFLOW_HOME'] = str(airflow_home)
    print_success(f"AIRFLOW_HOME: {airflow_home}")
    
    # Inicializar base de datos de Airflow
    if not run_command(
        ["airflow", "db", "init"],
        "Inicializar base de datos de Airflow"
    ):
        print_warning("Si Airflow no está instalado, ejecuta: pip install apache-airflow==2.8.1")
        return False
    
    # Crear usuario admin
    print("\n  Creando usuario administrador...")
    try:
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
        print_success("Usuario admin creado (usuario: admin, contraseña: admin)")
    except subprocess.CalledProcessError:
        print_warning("Usuario admin ya existe o hubo un error")
    
    return True


def print_next_steps():
    """Imprime los siguientes pasos."""
    next_steps = f"""
{Colors.GREEN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ✅ CONFIGURACIÓN COMPLETADA EXITOSAMENTE                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.END}

{Colors.BOLD}📋 SIGUIENTES PASOS:{Colors.END}

{Colors.YELLOW}1. Iniciar Airflow:{Colors.END}
   
   {Colors.BOLD}Terminal 1 (Scheduler):{Colors.END}
   $ airflow scheduler
   
   {Colors.BOLD}Terminal 2 (Webserver):{Colors.END}
   $ airflow webserver --port 8080

{Colors.YELLOW}2. Acceder a la Interfaz Web:{Colors.END}
   
   URL: {Colors.BLUE}http://localhost:8080{Colors.END}
   Usuario: {Colors.BOLD}admin{Colors.END}
   Contraseña: {Colors.BOLD}admin{Colors.END}

{Colors.YELLOW}3. Ejecutar el Pipeline:{Colors.END}
   
   - Busca el DAG: {Colors.BOLD}etl_sales_pipeline{Colors.END}
   - Activa el toggle (switch a ON)
   - Haz clic en ▶️ "Trigger DAG"

{Colors.YELLOW}4. Verificar Resultados:{Colors.END}
   
   $ sqlite3 data/database.db
   sqlite> SELECT * FROM sales_transformed LIMIT 5;

{Colors.BOLD}📚 DOCUMENTACIÓN:{Colors.END}
   - README.md: Documentación completa
   - QUICKSTART.md: Guía de inicio rápido
   - CONTRIBUTING.md: Guía de contribución

{Colors.BOLD}🔧 COMANDOS ÚTILES:{Colors.END}
   - make help: Ver todos los comandos disponibles
   - make test: Ejecutar tests
   - make run-pipeline: Ejecutar pipeline sin Airflow

{Colors.GREEN}¡Disfruta del proyecto! 🚀{Colors.END}
    """
    print(next_steps)


def main():
    """Función principal."""
    print_banner()
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Ejecutar pasos
    steps = [
        ("Instalar dependencias", install_dependencies),
        ("Crear directorios", create_directories),
        ("Configurar entorno", setup_environment),
        ("Crear base de datos", create_database),
        ("Inicializar Airflow", initialize_airflow),
    ]
    
    for step_name, step_func in steps:
        try:
            if not step_func():
                print_error(f"\nFalló el paso: {step_name}")
                print_error("Configuración interrumpida. Revisa los errores arriba.")
                sys.exit(1)
        except KeyboardInterrupt:
            print_error("\n\nConfiguración cancelada por el usuario.")
            sys.exit(1)
        except Exception as e:
            print_error(f"\nError inesperado en {step_name}: {e}")
            sys.exit(1)
    
    # Imprimir siguientes pasos
    print_next_steps()
    
    # Preguntar si desea iniciar Airflow
    print(f"\n{Colors.BOLD}¿Deseas iniciar Airflow ahora? (s/n): {Colors.END}", end='')
    try:
        response = input().strip().lower()
        if response in ['s', 'si', 'y', 'yes']:
            print(f"\n{Colors.GREEN}Iniciando Airflow...{Colors.END}")
            print(f"{Colors.YELLOW}Presiona Ctrl+C para detener{Colors.END}\n")
            time.sleep(2)
            
            # Iniciar scheduler en background
            scheduler_process = subprocess.Popen(
                ["airflow", "scheduler"],
                env=os.environ
            )
            
            # Iniciar webserver
            try:
                subprocess.run(
                    ["airflow", "webserver", "--port", "8080"],
                    env=os.environ
                )
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Deteniendo Airflow...{Colors.END}")
                scheduler_process.terminate()
                print_success("Airflow detenido")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operación cancelada{Colors.END}")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
