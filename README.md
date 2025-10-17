# 🚀 Proyecto de Orquestación ETL con Apache Airflow

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Airflow](https://img.shields.io/badge/Airflow-2.8.1-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Educational-yellow.svg)

## 📋 Descripción

Proyecto educativo completo que demuestra el uso de **Apache Airflow** como orquestador de flujos de datos ETL (Extract, Transform, Load). Este proyecto implementa un pipeline de procesamiento de datos de ventas desde la extracción hasta la carga en una base de datos, mostrando las mejores prácticas en orquestación de datos.

### 🎯 Objetivos del Proyecto

- ✅ Demostrar el uso práctico de Apache Airflow
- ✅ Implementar un flujo ETL completo y funcional
- ✅ Mostrar buenas prácticas en organización de código
- ✅ Proporcionar documentación detallada y educativa
- ✅ Incluir configuración con Docker para fácil despliegue

---

## 🏗️ Arquitectura del Proyecto

```
┌─────────────────────────────────────────────────────────────┐
│                     APACHE AIRFLOW                          │
│                     (Orquestador)                           │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
   ┌─────────┐        ┌─────────┐        ┌─────────┐
   │ EXTRACT │───────▶│TRANSFORM│───────▶│  LOAD   │
   └─────────┘        └─────────┘        └─────────┘
        │                   │                   │
        ▼                   ▼                   ▼
   SQLite DB          Pandas DF           SQLite DB
   (Origen)          (Limpieza)          (Destino)
```

### Flujo de Datos

1. **Extract**: Extrae datos desde la base de datos SQLite de origen
2. **Transform**: Limpia, valida y transforma los datos usando pandas
3. **Load**: Carga los datos procesados en la tabla destino

---

## 📁 Estructura del Proyecto

```
airflow_project/
├── 📂 dags/                          # DAGs de Airflow
│   ├── __init__.py
│   └── etl_pipeline.py              # DAG principal del pipeline ETL
│
├── 📂 scripts/                       # Scripts modulares ETL
│   ├── __init__.py
│   ├── create_dummy_db.py           # Crea base de datos con datos dummy
│   ├── extract_data.py              # Script de extracción
│   ├── transform_data.py            # Script de transformación
│   └── load_data.py                 # Script de carga
│
├── 📂 config/                        # Configuración del proyecto
│   ├── __init__.py
│   └── db_config.py                 # Configuración de base de datos
│
├── 📂 data/                          # Datos del proyecto
│   ├── input/                       # Datos de entrada
│   │   ├── .gitkeep
│   │   └── dummy_data.csv          # Datos de ejemplo (generado)
│   ├── output/                      # Datos procesados
│   │   ├── .gitkeep
│   │   ├── extracted_data.csv      # Datos extraídos (generado)
│   │   └── transformed_data.csv    # Datos transformados (generado)
│   └── database.db                  # Base de datos SQLite (generado)
│
├── 📂 docker/                        # Configuración de Docker
│   ├── Dockerfile                   # Imagen personalizada de Airflow
│   ├── docker-compose.yml           # Orquestación de contenedores
│   └── .env.docker                  # Variables de entorno para Docker
│
├── 📂 .github/                       # GitHub Actions
│   └── workflows/
│       └── ci.yml                   # Pipeline de CI/CD
│
├── 📂 airflow/                       # Directorio de Airflow (generado)
│   ├── logs/                        # Logs de ejecución
│   ├── airflow.db                   # Base de datos de metadatos
│   └── airflow.cfg                  # Configuración de Airflow
│
├── 📄 requirements.txt               # Dependencias de Python
├── 📄 .env                          # Variables de entorno (local)
├── 📄 .env.example                  # Ejemplo de variables de entorno
├── 📄 .gitignore                    # Archivos ignorados por Git
├── 📄 LICENSE                       # Licencia MIT
└── 📄 README.md                     # Este archivo
```

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.11 | Lenguaje principal |
| **Apache Airflow** | 2.8.1 | Orquestador de flujos |
| **Pandas** | 2.1.4 | Procesamiento de datos |
| **SQLite** | 3.x | Base de datos |
| **Docker** | Latest | Contenedorización |
| **Docker Compose** | Latest | Orquestación de contenedores |

---

## 🚀 Instalación y Configuración

### Opción 1: Instalación Local (Sin Docker)

#### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/Orquestador_Model_IA.git
cd Orquestador_Model_IA
```

#### Paso 2: Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### Paso 3: Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Paso 4: Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con las rutas correctas de tu sistema
# En Windows, usa rutas absolutas como: D:/GitHub/Orquestador_Model_IA
```

#### Paso 5: Inicializar Base de Datos Dummy

```bash
python scripts/create_dummy_db.py
```

**Salida esperada:**
```
============================================================
INICIANDO CREACIÓN DE BASE DE DATOS DUMMY
============================================================
Generando 1000 registros de datos dummy...
Datos generados exitosamente: (1000, 11)
Creando tablas en la base de datos...
Tabla 'sales_data' creada exitosamente
Tabla 'sales_transformed' creada exitosamente
Insertando datos en la base de datos...
1000 registros insertados en 'sales_data'
============================================================
✓ Base de datos creada exitosamente
✓ Total de registros en BD: 1000
✓ Ubicación: d:/GitHub/Orquestador_Model_IA/data/database.db
============================================================
```

#### Paso 6: Configurar Airflow

```bash
# Establecer AIRFLOW_HOME
export AIRFLOW_HOME=$(pwd)/airflow  # Linux/Mac
set AIRFLOW_HOME=%cd%\airflow       # Windows CMD
$env:AIRFLOW_HOME="$PWD\airflow"    # Windows PowerShell

# Inicializar base de datos de Airflow
airflow db init

# Crear usuario administrador
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

#### Paso 7: Iniciar Airflow

```bash
# Terminal 1: Iniciar el Scheduler
airflow scheduler

# Terminal 2: Iniciar el Webserver
airflow webserver --port 8080
```

#### Paso 8: Acceder a la Interfaz Web

Abre tu navegador y ve a: **http://localhost:8080**

- **Usuario**: `admin`
- **Contraseña**: `admin`

---

### Opción 2: Instalación con Docker 🐳

#### Paso 1: Requisitos Previos

- Docker Desktop instalado
- Docker Compose instalado

#### Paso 2: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/Orquestador_Model_IA.git
cd Orquestador_Model_IA
```

#### Paso 3: Configurar Variables de Entorno

```bash
cd docker
cp .env.docker .env
```

#### Paso 4: Inicializar Base de Datos Dummy (Opcional)

```bash
# Volver al directorio raíz
cd ..

# Crear entorno virtual temporal
python -m venv temp_venv
temp_venv\Scripts\activate  # Windows
# source temp_venv/bin/activate  # Linux/Mac

# Instalar dependencias mínimas
pip install pandas python-dotenv

# Crear base de datos
python scripts/create_dummy_db.py

# Desactivar entorno
deactivate
```

#### Paso 5: Iniciar Servicios con Docker Compose

```bash
cd docker
docker-compose up -d
```

**Servicios que se iniciarán:**
- `postgres`: Base de datos para metadatos de Airflow
- `airflow-init`: Inicialización de Airflow
- `airflow-webserver`: Interfaz web (puerto 8080)
- `airflow-scheduler`: Programador de tareas

#### Paso 6: Verificar Estado de los Contenedores

```bash
docker-compose ps
```

#### Paso 7: Acceder a la Interfaz Web

Abre tu navegador y ve a: **http://localhost:8080**

- **Usuario**: `airflow`
- **Contraseña**: `airflow`

#### Comandos Útiles de Docker

```bash
# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Eliminar todo (incluyendo volúmenes)
docker-compose down -v
```

---

## 📊 Uso del Pipeline ETL

### 1. Activar el DAG

1. Accede a la interfaz web de Airflow
2. Busca el DAG llamado `etl_sales_pipeline`
3. Activa el toggle en la columna "Active"

### 2. Ejecutar Manualmente

1. Haz clic en el nombre del DAG
2. Haz clic en el botón "Trigger DAG" (▶️)
3. Confirma la ejecución

### 3. Monitorear la Ejecución

#### Vista de Grafo (Graph View)
```
[start_pipeline] → [extract_data] → [transform_data] → [load_data] → [generate_report] → [end_pipeline]
```

- **Verde**: Tarea completada exitosamente
- **Rojo**: Tarea fallida
- **Amarillo**: Tarea en ejecución
- **Gris**: Tarea pendiente

#### Ver Logs de una Tarea

1. Haz clic en la tarea en el grafo
2. Selecciona "Log"
3. Revisa la salida detallada

### 4. Verificar Resultados

#### Opción A: Desde la Base de Datos

```bash
# Conectar a SQLite
sqlite3 data/database.db

# Ver datos transformados
SELECT * FROM sales_transformed LIMIT 10;

# Ver estadísticas
SELECT 
    COUNT(*) as total_records,
    SUM(total_venta) as total_sales,
    AVG(precio_promedio) as avg_price
FROM sales_transformed;

# Salir
.quit
```

#### Opción B: Desde los Archivos CSV

```bash
# Ver datos extraídos
cat data/output/extracted_data.csv | head

# Ver datos transformados
cat data/output/transformed_data.csv | head
```

#### Opción C: Con Python/Pandas

```python
import pandas as pd

# Leer datos transformados
df = pd.read_csv('data/output/transformed_data.csv')

# Ver primeras filas
print(df.head())

# Ver estadísticas
print(df.describe())

# Ver totales por región
print(df.groupby('region')['total_venta'].sum())
```

---

## 🔧 Configuración Avanzada

### Programación del DAG

El DAG está configurado para ejecutarse diariamente a medianoche. Para cambiar la frecuencia:

```python
# En dags/etl_pipeline.py
schedule_interval='0 0 * * *',  # Cron expression

# Ejemplos:
# '0 */6 * * *'   - Cada 6 horas
# '0 0 * * 1'     - Cada lunes
# '@hourly'       - Cada hora
# '@daily'        - Diario
# None            - Solo manual
```

### Variables de Airflow

Puedes configurar variables en la UI de Airflow:

1. Admin → Variables
2. Agregar nueva variable:
   - Key: `etl_batch_size`
   - Value: `1000`

Usar en el código:
```python
from airflow.models import Variable

batch_size = Variable.get("etl_batch_size", default_var=500)
```

### Conexiones

Para conectar a bases de datos externas:

1. Admin → Connections
2. Agregar nueva conexión
3. Configurar tipo, host, puerto, credenciales

---

## 📈 Descripción Detallada de los Scripts

### 1. `create_dummy_db.py`

**Propósito**: Genera datos de ventas simulados para demostración.

**Funcionalidades**:
- Genera 1000 registros de ventas con datos aleatorios
- Crea tablas `sales_data` (origen) y `sales_transformed` (destino)
- Incluye productos, categorías, regiones, precios, descuentos
- Agrega valores nulos intencionalmente para demostrar limpieza

**Datos generados**:
- 10 productos diferentes
- 4 categorías
- 5 regiones
- Rango de fechas: 2023
- Valores de venta: $10 - $1,500

### 2. `extract_data.py`

**Propósito**: Extrae datos desde la base de datos SQLite.

**Proceso**:
1. Conecta a la base de datos
2. Ejecuta query SELECT para extraer todos los registros
3. Valida los datos extraídos:
   - Verifica que no esté vacío
   - Valida columnas requeridas
   - Convierte tipos de datos
   - Reporta valores nulos
4. Guarda datos en `extracted_data.csv`
5. Genera resumen de extracción

**Validaciones**:
- ✅ DataFrame no vacío
- ✅ Columnas requeridas presentes
- ✅ Fechas en formato correcto
- ✅ Valores numéricos válidos

### 3. `transform_data.py`

**Propósito**: Limpia, valida y transforma los datos.

**Proceso de Limpieza**:
1. **Duplicados**: Elimina registros duplicados completos
2. **Valores nulos**: 
   - Rellena descuentos nulos con 0
   - Elimina filas con nulos en columnas críticas
3. **Validación numérica**:
   - Elimina cantidades ≤ 0
   - Elimina precios ≤ 0
4. **Outliers**: Usa método IQR (Interquartile Range) para detectar y eliminar outliers
5. **Normalización**: Normaliza texto (capitalización, espacios)

**Transformaciones**:
- Extrae componentes de fecha (año, mes, día, trimestre)
- Calcula métricas derivadas (ingreso bruto, descuento total, margen)
- Categoriza ventas (Pequeña, Mediana, Grande, Premium)
- Crea flags booleanos (tiene_descuento, venta_alta)

**Agregación**:
- Agrupa por: fecha, producto, categoría, región
- Suma cantidades
- Promedia precios y descuentos
- Cuenta número de transacciones

### 4. `load_data.py`

**Propósito**: Carga datos transformados en la base de datos destino.

**Proceso**:
1. Carga datos desde `transformed_data.csv`
2. Valida datos antes de la carga:
   - Verifica que no esté vacío
   - Valida columnas requeridas
   - Verifica valores nulos en columnas críticas
   - Valida valores numéricos positivos
3. Prepara datos:
   - Convierte fechas a formato string
   - Asegura tipos de datos correctos
   - Ordena por fecha
4. Crea backup de datos existentes (opcional)
5. Inserta datos en tabla `sales_transformed`
6. Crea índices para optimizar consultas
7. Genera estadísticas de carga

**Índices creados**:
- `idx_sales_transformed_fecha`
- `idx_sales_transformed_producto`
- `idx_sales_transformed_categoria`
- `idx_sales_transformed_region`

---

## 🧪 Testing

### Ejecutar Tests Unitarios

```bash
# Instalar pytest
pip install pytest pytest-cov

# Ejecutar todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=scripts --cov-report=html
```

### Probar Scripts Individualmente

```bash
# Probar extracción
python scripts/extract_data.py

# Probar transformación
python scripts/transform_data.py

# Probar carga
python scripts/load_data.py
```

### Probar DAG sin Ejecutar

```bash
# Verificar sintaxis del DAG
python dags/etl_pipeline.py

# Listar DAGs
airflow dags list

# Probar DAG (sin ejecutar)
airflow dags test etl_sales_pipeline 2025-01-01

# Probar una tarea específica
airflow tasks test etl_sales_pipeline extract_data 2025-01-01
```

---

## 📊 Métricas y Monitoreo

### Métricas del Pipeline

El pipeline genera las siguientes métricas:

1. **Extracción**:
   - Total de registros extraídos
   - Rango de fechas
   - Total de ventas
   - Valores nulos encontrados

2. **Transformación**:
   - Registros originales vs transformados
   - Porcentaje de reducción
   - Registros eliminados por limpieza
   - Outliers removidos

3. **Carga**:
   - Registros cargados
   - Total de ventas en destino
   - Top 5 productos
   - Top 5 regiones

### Logs

Los logs se encuentran en:
- **Local**: `airflow/logs/dag_id/task_id/execution_date/`
- **Docker**: Accesibles vía `docker-compose logs`

### Alertas

Configurar alertas por email en caso de fallo:

```python
# En default_args del DAG
'email': ['tu-email@example.com'],
'email_on_failure': True,
'email_on_retry': True,
```

---

## 🐛 Troubleshooting

### Problema: Airflow no encuentra los DAGs

**Solución**:
```bash
# Verificar AIRFLOW_HOME
echo $AIRFLOW_HOME  # Linux/Mac
echo %AIRFLOW_HOME%  # Windows

# Verificar configuración
airflow config get-value core dags_folder

# Listar DAGs
airflow dags list
```

### Problema: Error de importación de módulos

**Solución**:
```bash
# Agregar directorio al PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%cd%  # Windows
```

### Problema: Base de datos no existe

**Solución**:
```bash
# Ejecutar script de creación
python scripts/create_dummy_db.py

# Verificar que se creó
ls -la data/database.db  # Linux/Mac
dir data\database.db  # Windows
```

### Problema: Permisos en Docker

**Solución**:
```bash
# Linux/Mac: Usar tu UID
echo -e "AIRFLOW_UID=$(id -u)" > docker/.env

# Windows: Usar 50000
echo AIRFLOW_UID=50000 > docker/.env
```

### Problema: Puerto 8080 en uso

**Solución**:
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8081:8080"  # Usar 8081 en lugar de 8080

# O detener el proceso que usa el puerto
# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8080 | xargs kill -9
```

---

## 🔒 Mejores Prácticas

### Seguridad

1. **No commitear credenciales**: Usa `.env` y `.gitignore`
2. **Usar Secrets**: Para producción, usa Airflow Secrets Backend
3. **Validar inputs**: Siempre valida datos antes de procesarlos
4. **Logs seguros**: No loguear información sensible

### Rendimiento

1. **Batch processing**: Procesa datos en lotes
2. **Índices**: Crea índices en columnas frecuentemente consultadas
3. **Paralelización**: Usa `max_active_runs` y `concurrency`
4. **Limpieza**: Elimina logs antiguos regularmente

### Mantenibilidad

1. **Código modular**: Separa lógica en funciones reutilizables
2. **Documentación**: Documenta DAGs y funciones
3. **Testing**: Escribe tests para funciones críticas
4. **Versionado**: Usa Git para control de versiones

---

## 📚 Recursos Adicionales

### Documentación Oficial

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

### Tutoriales Recomendados

- [Airflow Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)
- [ETL Best Practices](https://www.astronomer.io/guides/)
- [Data Pipeline Design Patterns](https://www.oreilly.com/library/view/data-pipelines-pocket/9781492087823/)

### Comunidad

- [Airflow Slack](https://apache-airflow.slack.com/)
- [Stack Overflow - Airflow Tag](https://stackoverflow.com/questions/tagged/airflow)
- [Reddit - r/dataengineering](https://www.reddit.com/r/dataengineering/)

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Changelog

### Version 1.0.0 (2025-01-15)
- ✨ Implementación inicial del proyecto
- ✨ Pipeline ETL completo con Airflow
- ✨ Scripts modulares de extracción, transformación y carga
- ✨ Configuración con Docker
- ✨ Documentación completa
- ✨ Datos dummy para demostración

---

## 👥 Autores

- **Proyecto Educativo ETL** - *Trabajo Inicial* - [GitHub](https://github.com/tu-usuario)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- Apache Airflow Community
- Pandas Development Team
- Todos los contribuidores de código abierto

---

## 📞 Contacto

¿Preguntas o sugerencias? Abre un [issue](https://github.com/tu-usuario/Orquestador_Model_IA/issues) en GitHub.

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐**

Made with ❤️ for the Data Engineering Community

</div>
