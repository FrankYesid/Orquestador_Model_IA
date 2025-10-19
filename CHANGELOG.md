# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

### Planeado
- Agregar soporte para PostgreSQL como base de datos de origen
- Implementar notificaciones por email en caso de fallo
- Agregar dashboard de visualización con Plotly
- Implementar tests de integración completos
- Agregar soporte para procesamiento en paralelo

## [1.0.0] - 2025-01-15

### Agregado
- ✨ Pipeline ETL completo con Apache Airflow
- ✨ Script de extracción de datos desde SQLite (`extract_data.py`)
- ✨ Script de transformación con limpieza y agregación (`transform_data.py`)
- ✨ Script de carga a base de datos destino (`load_data.py`)
- ✨ DAG de Airflow con 6 tareas orquestadas (`etl_pipeline.py`)
- ✨ Script para generar base de datos dummy (`create_dummy_db.py`)
- ✨ Configuración completa de Docker y Docker Compose
- ✨ Módulo de configuración de base de datos (`db_config.py`)
- ✨ Sistema de logging detallado en todos los scripts
- ✨ Validación de datos en cada etapa del pipeline
- ✨ Manejo de errores y reintentos en Airflow
- ✨ Generación de estadísticas y reportes
- ✨ Creación de índices para optimización de consultas
- ✨ Sistema de backup de datos antes de carga

### Documentación
- 📚 README.md completo con guías detalladas
- 📚 QUICKSTART.md para inicio rápido
- 📚 CONTRIBUTING.md con guías de contribución
- 📚 Documentación inline en todos los scripts
- 📚 Docstrings en formato Google para todas las funciones
- 📚 Ejemplos de uso y casos de prueba

### Configuración
- ⚙️ requirements.txt con todas las dependencias
- ⚙️ .env y .env.example para variables de entorno
- ⚙️ .gitignore configurado para Python y Airflow
- ⚙️ Dockerfile para imagen personalizada de Airflow
- ⚙️ docker-compose.yml con servicios completos
- ⚙️ Makefile con comandos útiles
- ⚙️ setup.py para instalación del paquete
- ⚙️ pytest.ini para configuración de tests
- ⚙️ .editorconfig para consistencia de código

### Tests
- 🧪 Tests unitarios para extracción (`test_extract.py`)
- 🧪 Tests unitarios para transformación (`test_transform.py`)
- 🧪 Tests unitarios para carga (`test_load.py`)
- 🧪 Configuración de pytest con cobertura

### CI/CD
- 🔄 GitHub Actions workflow para CI/CD
- 🔄 Linting automático con flake8
- 🔄 Formateo con black e isort
- 🔄 Ejecución automática de tests

### Características del Pipeline
- 📊 Extracción de 1000+ registros de ventas
- 📊 Limpieza de valores nulos y duplicados
- 📊 Detección y eliminación de outliers usando IQR
- 📊 Agregación por producto, categoría y región
- 📊 Cálculo de métricas derivadas
- 📊 Categorización automática de ventas
- 📊 Generación de componentes de fecha
- 📊 Validación de datos en múltiples etapas

### Seguridad
- 🔒 Variables de entorno para credenciales
- 🔒 .gitignore para archivos sensibles
- 🔒 Validación de inputs en todos los scripts

### Rendimiento
- ⚡ Procesamiento por lotes (batch processing)
- ⚡ Índices en columnas frecuentemente consultadas
- ⚡ Optimización de queries SQL
- ⚡ Uso eficiente de memoria con pandas

## [0.1.0] - 2025-01-01

### Agregado
- 🎉 Inicio del proyecto
- 🎉 Estructura básica de directorios
- 🎉 Configuración inicial de Git

---

## Tipos de Cambios

- `Agregado` para nuevas funcionalidades
- `Cambiado` para cambios en funcionalidades existentes
- `Deprecado` para funcionalidades que serán eliminadas
- `Eliminado` para funcionalidades eliminadas
- `Corregido` para corrección de bugs
- `Seguridad` para vulnerabilidades corregidas

---

## Versionado

Este proyecto usa [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.x.x): Cambios incompatibles con versiones anteriores
- **MINOR** (x.1.x): Nuevas funcionalidades compatibles
- **PATCH** (x.x.1): Correcciones de bugs compatibles

---

[Unreleased]: https://github.com/tu-usuario/Orquestador_Model_IA/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/tu-usuario/Orquestador_Model_IA/releases/tag/v1.0.0
[0.1.0]: https://github.com/tu-usuario/Orquestador_Model_IA/releases/tag/v0.1.0
