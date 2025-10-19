# ⚡ Guía de Inicio Rápido

Esta guía te ayudará a poner en marcha el proyecto en **menos de 10 minutos**.

## 🎯 Opción 1: Inicio Rápido Local (Recomendado para Windows)

### Paso 1: Requisitos Previos

- ✅ Python 3.11 instalado
- ✅ Git instalado

### Paso 2: Clonar y Configurar (2 minutos)

```powershell
# Clonar el repositorio
git clone https://github.com/tu-usuario/Orquestador_Model_IA.git
cd Orquestador_Model_IA

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 3: Crear Base de Datos (1 minuto)

```powershell
python scripts/create_dummy_db.py
```

**✅ Salida esperada:**
```
============================================================
✓ Base de datos creada exitosamente
✓ Total de registros en BD: 1000
============================================================
```

### Paso 4: Configurar Airflow (2 minutos)

```powershell
# Establecer AIRFLOW_HOME
$env:AIRFLOW_HOME="$PWD\airflow"

# Inicializar Airflow
airflow db init

# Crear usuario admin
airflow users create `
    --username admin `
    --firstname Admin `
    --lastname User `
    --role Admin `
    --email admin@example.com `
    --password admin
```

### Paso 5: Iniciar Airflow (1 minuto)

**Terminal 1 - Scheduler:**
```powershell
airflow scheduler
```

**Terminal 2 - Webserver:**
```powershell
airflow webserver --port 8080
```

### Paso 6: Acceder a Airflow

1. Abre tu navegador: **http://localhost:8080**
2. Login:
   - **Usuario:** `admin`
   - **Contraseña:** `admin`

### Paso 7: Ejecutar el Pipeline

1. Busca el DAG: `etl_sales_pipeline`
2. Activa el toggle (switch a ON)
3. Haz clic en el botón ▶️ "Trigger DAG"
4. ¡Listo! Observa la ejecución en tiempo real

---

## 🐳 Opción 2: Inicio Rápido con Docker (Recomendado para Linux/Mac)

### Paso 1: Requisitos Previos

- ✅ Docker instalado
- ✅ Docker Compose instalado

### Paso 2: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/Orquestador_Model_IA.git
cd Orquestador_Model_IA
```

### Paso 3: Configurar Variables de Entorno

```bash
cd docker
cp .env.docker .env

# Linux/Mac: Configurar UID
echo "AIRFLOW_UID=$(id -u)" >> .env
```

### Paso 4: Crear Base de Datos (Opcional)

```bash
cd ..
python3 -m venv temp_venv
source temp_venv/bin/activate
pip install pandas python-dotenv
python scripts/create_dummy_db.py
deactivate
```

### Paso 5: Iniciar Servicios

```bash
cd docker
docker-compose up -d
```

**Espera 2-3 minutos** para que los servicios se inicialicen.

### Paso 6: Verificar Estado

```bash
docker-compose ps
```

Todos los servicios deben estar "Up" y "healthy".

### Paso 7: Acceder a Airflow

1. Abre tu navegador: **http://localhost:8080**
2. Login:
   - **Usuario:** `airflow`
   - **Contraseña:** `airflow`

---

## 🎨 Interfaz de Airflow - Guía Visual

### Vista Principal (DAGs)

```
┌─────────────────────────────────────────────────────────┐
│ Apache Airflow                                    admin ▼│
├─────────────────────────────────────────────────────────┤
│ DAGs  │  Browse  │  Admin  │  Docs                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ 🔍 Search DAGs...                                        │
│                                                          │
│ ┌──────────────────────────────────────────────────┐   │
│ │ etl_sales_pipeline                    ⚪→🟢      │   │
│ │ Pipeline ETL para procesar datos de ventas       │   │
│ │ Tags: etl, sales, data-pipeline                  │   │
│ │ Schedule: 0 0 * * * (Daily)                      │   │
│ │ Last Run: Success ✓                              │   │
│ │ [▶️ Trigger] [📊 Graph] [📋 Logs]                │   │
│ └──────────────────────────────────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Vista de Grafo (Graph View)

```
start_pipeline
      ↓
extract_data
      ↓
transform_data
      ↓
load_data
      ↓
generate_report
      ↓
end_pipeline
```

**Colores de Estado:**
- 🟢 Verde: Éxito
- 🔴 Rojo: Error
- 🟡 Amarillo: En ejecución
- ⚪ Gris: Pendiente

---

## 📊 Verificar Resultados

### Opción A: Consultar la Base de Datos

```powershell
# Abrir SQLite
sqlite3 data/database.db

# Ver datos transformados
SELECT * FROM sales_transformed LIMIT 5;

# Ver estadísticas
SELECT 
    COUNT(*) as total_registros,
    SUM(total_venta) as ventas_totales,
    AVG(precio_promedio) as precio_promedio
FROM sales_transformed;

# Salir
.quit
```

### Opción B: Ver Archivos CSV

```powershell
# Ver datos extraídos
type data\output\extracted_data.csv | Select-Object -First 10

# Ver datos transformados
type data\output\transformed_data.csv | Select-Object -First 10
```

### Opción C: Con Python

```python
import pandas as pd

# Leer datos transformados
df = pd.read_csv('data/output/transformed_data.csv')

# Mostrar primeras filas
print(df.head())

# Estadísticas básicas
print(df.describe())

# Ventas por región
print(df.groupby('region')['total_venta'].sum().sort_values(ascending=False))
```

---

## 🔧 Comandos Útiles

### Airflow CLI

```powershell
# Listar DAGs
airflow dags list

# Ver estado de un DAG
airflow dags state etl_sales_pipeline

# Probar una tarea
airflow tasks test etl_sales_pipeline extract_data 2025-01-01

# Ver logs
airflow tasks logs etl_sales_pipeline extract_data 2025-01-01
```

### Scripts Individuales

```powershell
# Ejecutar solo extracción
python scripts/extract_data.py

# Ejecutar solo transformación
python scripts/transform_data.py

# Ejecutar solo carga
python scripts/load_data.py
```

### Docker

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f airflow-webserver

# Reiniciar servicios
docker-compose restart

# Detener servicios
docker-compose down

# Eliminar todo (incluyendo datos)
docker-compose down -v
```

---

## ❓ Solución de Problemas Comunes

### Problema: "No module named 'airflow'"

**Solución:**
```powershell
# Verificar que el entorno virtual esté activado
venv\Scripts\activate

# Reinstalar Airflow
pip install apache-airflow==2.8.1
```

### Problema: "Port 8080 already in use"

**Solución:**
```powershell
# Cambiar puerto
airflow webserver --port 8081

# O detener el proceso que usa el puerto
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

### Problema: DAG no aparece en la UI

**Solución:**
```powershell
# Verificar AIRFLOW_HOME
echo $env:AIRFLOW_HOME

# Verificar que el DAG esté en la carpeta correcta
ls dags\

# Verificar errores en el DAG
airflow dags list-import-errors

# Refrescar DAGs (esperar 30 segundos)
```

### Problema: Base de datos no existe

**Solución:**
```powershell
# Crear la base de datos
python scripts/create_dummy_db.py

# Verificar que se creó
ls data\database.db
```

### Problema: Permisos en Docker (Linux/Mac)

**Solución:**
```bash
# Configurar UID correcto
echo "AIRFLOW_UID=$(id -u)" > docker/.env

# Reiniciar servicios
cd docker
docker-compose down
docker-compose up -d
```

---

## 📚 Próximos Pasos

Una vez que el pipeline esté funcionando:

1. **Explorar el código:**
   - Lee `dags/etl_pipeline.py` para entender el DAG
   - Revisa `scripts/extract_data.py`, `transform_data.py`, `load_data.py`

2. **Modificar el pipeline:**
   - Cambia la frecuencia de ejecución
   - Agrega nuevas transformaciones
   - Crea nuevas tareas

3. **Experimentar:**
   - Genera más datos dummy
   - Modifica los filtros de extracción
   - Agrega nuevas métricas

4. **Aprender más:**
   - Lee el [README.md](README.md) completo
   - Consulta la [documentación de Airflow](https://airflow.apache.org/docs/)
   - Revisa [CONTRIBUTING.md](CONTRIBUTING.md) para contribuir

---

## 🎉 ¡Felicidades!

Has configurado exitosamente un pipeline ETL con Apache Airflow. 

**¿Necesitas ayuda?** Abre un [issue en GitHub](https://github.com/tu-usuario/Orquestador_Model_IA/issues)

---

## 📋 Checklist de Verificación

- [ ] Python 3.11 instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Base de datos creada (`python scripts/create_dummy_db.py`)
- [ ] Airflow inicializado (`airflow db init`)
- [ ] Usuario admin creado
- [ ] Scheduler ejecutándose
- [ ] Webserver ejecutándose
- [ ] Acceso a UI (http://localhost:8080)
- [ ] DAG visible en la UI
- [ ] DAG activado
- [ ] Pipeline ejecutado exitosamente
- [ ] Resultados verificados

**¡Todo listo! 🚀**
