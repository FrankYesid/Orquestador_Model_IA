# 🔧 Guía de Solución de Problemas

Esta guía te ayudará a resolver los problemas más comunes al trabajar con el proyecto ETL de Apache Airflow.

---

## 📑 Tabla de Contenidos

1. [Problemas de Instalación](#problemas-de-instalación)
2. [Problemas con Airflow](#problemas-con-airflow)
3. [Problemas con la Base de Datos](#problemas-con-la-base-de-datos)
4. [Problemas con Docker](#problemas-con-docker)
5. [Problemas con el Pipeline](#problemas-con-el-pipeline)
6. [Problemas de Rendimiento](#problemas-de-rendimiento)
7. [Errores Comunes](#errores-comunes)

---

## Problemas de Instalación

### ❌ Error: "No module named 'airflow'"

**Causa**: Apache Airflow no está instalado o el entorno virtual no está activado.

**Solución**:

```powershell
# Windows
venv\Scripts\activate
pip install apache-airflow==2.8.1

# Linux/Mac
source venv/bin/activate
pip install apache-airflow==2.8.1
```

### ❌ Error: "Python version 3.11+ required"

**Causa**: Versión de Python incompatible.

**Solución**:

1. Descarga Python 3.11 o superior desde [python.org](https://www.python.org/downloads/)
2. Instala y verifica:
   ```bash
   python --version
   ```

### ❌ Error: "pip: command not found"

**Causa**: pip no está instalado o no está en el PATH.

**Solución**:

```bash
# Instalar pip
python -m ensurepip --upgrade

# Verificar instalación
python -m pip --version
```

### ❌ Error al instalar dependencias en Windows

**Causa**: Falta compilador de C++ para algunas dependencias.

**Solución**:

1. Instala [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. O usa versiones pre-compiladas:
   ```bash
   pip install --only-binary :all: -r requirements.txt
   ```

---

## Problemas con Airflow

### ❌ Error: "AIRFLOW_HOME not set"

**Causa**: Variable de entorno AIRFLOW_HOME no configurada.

**Solución**:

```powershell
# Windows PowerShell
$env:AIRFLOW_HOME="$PWD\airflow"

# Windows CMD
set AIRFLOW_HOME=%cd%\airflow

# Linux/Mac
export AIRFLOW_HOME=$(pwd)/airflow
```

### ❌ Error: "DAG not found"

**Causa**: Airflow no puede encontrar los DAGs.

**Solución**:

1. Verificar configuración:
   ```bash
   airflow config get-value core dags_folder
   ```

2. Verificar que el DAG esté en la carpeta correcta:
   ```bash
   ls dags/etl_pipeline.py
   ```

3. Verificar errores de importación:
   ```bash
   airflow dags list-import-errors
   ```

4. Refrescar DAGs (esperar 30 segundos)

### ❌ Error: "Port 8080 already in use"

**Causa**: Otro proceso está usando el puerto 8080.

**Solución**:

**Opción 1: Cambiar puerto**
```bash
airflow webserver --port 8081
```

**Opción 2: Detener proceso que usa el puerto**

```powershell
# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8080 | xargs kill -9
```

### ❌ Error: "Airflow database not initialized"

**Causa**: Base de datos de Airflow no inicializada.

**Solución**:

```bash
airflow db init
```

### ❌ Error: "No such table: dag_run"

**Causa**: Base de datos de Airflow corrupta o no inicializada correctamente.

**Solución**:

```bash
# Eliminar base de datos
rm airflow/airflow.db

# Reinicializar
airflow db init

# Recrear usuario
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

### ❌ DAG aparece pero no se ejecuta

**Causa**: DAG pausado o schedule_interval incorrecto.

**Solución**:

1. Verificar que el DAG esté activado (toggle en ON)
2. Verificar schedule_interval en el código
3. Ejecutar manualmente con "Trigger DAG"
4. Revisar logs del scheduler:
   ```bash
   tail -f airflow/logs/scheduler/latest/*.log
   ```

---

## Problemas con la Base de Datos

### ❌ Error: "database.db not found"

**Causa**: Base de datos dummy no creada.

**Solución**:

```bash
python scripts/create_dummy_db.py
```

### ❌ Error: "no such table: sales_data"

**Causa**: Tablas no creadas en la base de datos.

**Solución**:

```bash
# Eliminar base de datos existente
rm data/database.db

# Recrear
python scripts/create_dummy_db.py
```

### ❌ Error: "database is locked"

**Causa**: Múltiples procesos intentando acceder a SQLite simultáneamente.

**Solución**:

1. Cerrar todos los procesos que usan la base de datos
2. Usar PostgreSQL en lugar de SQLite para producción
3. Aumentar timeout en db_config.py:
   ```python
   conn = sqlite3.connect(self.db_path, timeout=30)
   ```

### ❌ Error: "unable to open database file"

**Causa**: Permisos incorrectos o ruta inválida.

**Solución**:

```bash
# Verificar permisos
ls -la data/database.db

# Dar permisos (Linux/Mac)
chmod 666 data/database.db

# Verificar ruta en .env
cat .env | grep DB_PATH
```

---

## Problemas con Docker

### ❌ Error: "docker: command not found"

**Causa**: Docker no instalado.

**Solución**:

1. Instala [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Verifica instalación:
   ```bash
   docker --version
   docker-compose --version
   ```

### ❌ Error: "permission denied" en Linux/Mac

**Causa**: Usuario no tiene permisos para Docker.

**Solución**:

```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Cerrar sesión y volver a iniciar
# O ejecutar:
newgrp docker
```

### ❌ Error: "AIRFLOW_UID not set"

**Causa**: Variable AIRFLOW_UID no configurada.

**Solución**:

```bash
# Linux/Mac
echo "AIRFLOW_UID=$(id -u)" > docker/.env

# Windows
echo AIRFLOW_UID=50000 > docker/.env
```

### ❌ Contenedores no inician

**Causa**: Recursos insuficientes o conflictos de puertos.

**Solución**:

1. Verificar recursos de Docker Desktop (mínimo 4GB RAM)
2. Verificar logs:
   ```bash
   cd docker
   docker-compose logs
   ```
3. Reiniciar servicios:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

### ❌ Error: "network not found"

**Causa**: Red de Docker no creada.

**Solución**:

```bash
cd docker
docker-compose down
docker network prune
docker-compose up -d
```

---

## Problemas con el Pipeline

### ❌ Tarea "extract_data" falla

**Posibles causas y soluciones**:

1. **Base de datos no existe**:
   ```bash
   python scripts/create_dummy_db.py
   ```

2. **Permisos de lectura**:
   ```bash
   # Linux/Mac
   chmod 644 data/database.db
   ```

3. **Ruta incorrecta en .env**:
   Verificar DB_PATH en archivo .env

### ❌ Tarea "transform_data" falla

**Posibles causas y soluciones**:

1. **Archivo extracted_data.csv no existe**:
   - Ejecutar primero extract_data
   - Verificar data/output/extracted_data.csv

2. **Datos corruptos**:
   ```bash
   # Verificar archivo
   head data/output/extracted_data.csv
   ```

3. **Memoria insuficiente**:
   - Reducir BATCH_SIZE en .env
   - Aumentar memoria disponible

### ❌ Tarea "load_data" falla

**Posibles causas y soluciones**:

1. **Archivo transformed_data.csv no existe**:
   - Ejecutar primero transform_data
   - Verificar data/output/transformed_data.csv

2. **Base de datos bloqueada**:
   - Cerrar otras conexiones a la BD
   - Reiniciar el pipeline

3. **Validación falla**:
   - Revisar logs para ver qué validación falló
   - Verificar datos en transformed_data.csv

### ❌ Pipeline se ejecuta pero no genera resultados

**Solución**:

1. Verificar logs de cada tarea en la UI de Airflow
2. Ejecutar scripts individualmente:
   ```bash
   python scripts/extract_data.py
   python scripts/transform_data.py
   python scripts/load_data.py
   ```
3. Verificar permisos de escritura en data/output/

---

## Problemas de Rendimiento

### ⚠️ Pipeline muy lento

**Soluciones**:

1. **Aumentar paralelismo** en airflow.cfg:
   ```ini
   [core]
   parallelism = 32
   max_active_runs_per_dag = 3
   ```

2. **Optimizar consultas SQL**:
   - Agregar índices
   - Limitar cantidad de datos procesados

3. **Usar PostgreSQL** en lugar de SQLite:
   - Mejor rendimiento para concurrencia
   - Configurar en docker-compose.yml

### ⚠️ Alto uso de memoria

**Soluciones**:

1. **Procesar en lotes**:
   ```python
   # En transform_data.py
   chunk_size = 1000
   for chunk in pd.read_csv(file, chunksize=chunk_size):
       process_chunk(chunk)
   ```

2. **Limpiar datos intermedios**:
   ```bash
   rm data/output/*.csv
   ```

3. **Aumentar recursos de Docker**:
   - Docker Desktop → Settings → Resources
   - Aumentar Memory Limit

---

## Errores Comunes

### ❌ ImportError: cannot import name 'X'

**Causa**: Módulo no encontrado o versión incompatible.

**Solución**:

```bash
# Reinstalar dependencias
pip install --force-reinstall -r requirements.txt

# Verificar versiones
pip list | grep airflow
pip list | grep pandas
```

### ❌ ModuleNotFoundError: No module named 'scripts'

**Causa**: PYTHONPATH no configurado correctamente.

**Solución**:

```bash
# Agregar directorio raíz al PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%cd%  # Windows CMD
$env:PYTHONPATH="$env:PYTHONPATH;$PWD"  # Windows PowerShell
```

### ❌ FileNotFoundError: [Errno 2] No such file or directory

**Causa**: Rutas incorrectas o archivos faltantes.

**Solución**:

1. Verificar rutas en .env
2. Usar rutas absolutas
3. Crear directorios faltantes:
   ```bash
   mkdir -p data/input data/output airflow/logs
   ```

### ❌ PermissionError: [Errno 13] Permission denied

**Causa**: Permisos insuficientes.

**Solución**:

```bash
# Linux/Mac
chmod -R 755 data/
chmod -R 755 airflow/

# Windows: Ejecutar como Administrador
```

### ❌ UnicodeDecodeError

**Causa**: Problemas de codificación de archivos.

**Solución**:

```python
# Al leer archivos, especificar encoding
df = pd.read_csv(file_path, encoding='utf-8')
```

---

## 🆘 Obtener Ayuda

Si ninguna de estas soluciones funciona:

1. **Revisar logs detallados**:
   ```bash
   # Logs de Airflow
   tail -f airflow/logs/scheduler/latest/*.log
   
   # Logs de tareas
   airflow tasks logs etl_sales_pipeline extract_data 2025-01-01
   ```

2. **Ejecutar script de verificación**:
   ```bash
   python scripts/verify_installation.py
   ```

3. **Buscar en Issues de GitHub**:
   - Revisa [issues existentes](https://github.com/tu-usuario/Orquestador_Model_IA/issues)
   - Abre un nuevo issue con:
     - Descripción del problema
     - Logs de error
     - Pasos para reproducir
     - Sistema operativo y versiones

4. **Consultar documentación oficial**:
   - [Apache Airflow Docs](https://airflow.apache.org/docs/)
   - [Pandas Docs](https://pandas.pydata.org/docs/)
   - [SQLite Docs](https://www.sqlite.org/docs.html)

5. **Comunidad**:
   - [Stack Overflow - Airflow Tag](https://stackoverflow.com/questions/tagged/airflow)
   - [Airflow Slack](https://apache-airflow.slack.com/)
   - [Reddit r/dataengineering](https://www.reddit.com/r/dataengineering/)

---

## 🔄 Reinicio Completo

Si todo lo demás falla, reinicia el proyecto desde cero:

```bash
# 1. Limpiar todo
make clean
make clean-db
rm -rf airflow/
rm -rf venv/

# 2. Recrear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# 3. Reinstalar
pip install -r requirements.txt

# 4. Reconfigurar
python scripts/create_dummy_db.py
airflow db init
airflow users create --username admin --password admin --role Admin --email admin@example.com --firstname Admin --lastname User

# 5. Reiniciar Airflow
airflow scheduler &
airflow webserver
```

---

**¿Encontraste un problema no listado aquí?** 

Por favor, [abre un issue](https://github.com/tu-usuario/Orquestador_Model_IA/issues/new) para que podamos agregarlo a esta guía.
