@echo off
REM Script de Windows para ejecutar el pipeline ETL completo

echo ============================================================
echo   EJECUTANDO PIPELINE ETL
echo   Proyecto de Orquestacion con Apache Airflow
echo ============================================================
echo.

REM Activar entorno virtual si existe
if exist venv\Scripts\activate.bat (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
)

REM Establecer PYTHONPATH
set PYTHONPATH=%CD%

echo.
echo [1/3] Ejecutando Extraccion...
echo ------------------------------------------------------------
python scripts\extract_data.py
if %ERRORLEVEL% neq 0 (
    echo ERROR: Fallo en la extraccion
    pause
    exit /b 1
)

echo.
echo [2/3] Ejecutando Transformacion...
echo ------------------------------------------------------------
python scripts\transform_data.py
if %ERRORLEVEL% neq 0 (
    echo ERROR: Fallo en la transformacion
    pause
    exit /b 1
)

echo.
echo [3/3] Ejecutando Carga...
echo ------------------------------------------------------------
python scripts\load_data.py
if %ERRORLEVEL% neq 0 (
    echo ERROR: Fallo en la carga
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   PIPELINE COMPLETADO EXITOSAMENTE
echo ============================================================
echo.
echo Resultados disponibles en:
echo   - data\output\transformed_data.csv
echo   - Base de datos: data\database.db (tabla: sales_transformed)
echo.

pause
