#!/bin/bash
# Script de Linux/Mac para ejecutar el pipeline ETL completo

echo "============================================================"
echo "  EJECUTANDO PIPELINE ETL"
echo "  Proyecto de Orquestación con Apache Airflow"
echo "============================================================"
echo ""

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "Activando entorno virtual..."
    source venv/bin/activate
fi

# Establecer PYTHONPATH
export PYTHONPATH=$(pwd)

echo ""
echo "[1/3] Ejecutando Extracción..."
echo "------------------------------------------------------------"
python scripts/extract_data.py
if [ $? -ne 0 ]; then
    echo "ERROR: Falló en la extracción"
    exit 1
fi

echo ""
echo "[2/3] Ejecutando Transformación..."
echo "------------------------------------------------------------"
python scripts/transform_data.py
if [ $? -ne 0 ]; then
    echo "ERROR: Falló en la transformación"
    exit 1
fi

echo ""
echo "[3/3] Ejecutando Carga..."
echo "------------------------------------------------------------"
python scripts/load_data.py
if [ $? -ne 0 ]; then
    echo "ERROR: Falló en la carga"
    exit 1
fi

echo ""
echo "============================================================"
echo "  PIPELINE COMPLETADO EXITOSAMENTE"
echo "============================================================"
echo ""
echo "Resultados disponibles en:"
echo "  - data/output/transformed_data.csv"
echo "  - Base de datos: data/database.db (tabla: sales_transformed)"
echo ""
