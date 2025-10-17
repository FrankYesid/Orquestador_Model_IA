# Dockerfile para Apache Airflow con dependencias del proyecto ETL
# Basado en la imagen oficial de Apache Airflow

FROM apache/airflow:2.8.1-python3.11

# Información del mantenedor
LABEL maintainer="ETL Project Team"
LABEL description="Apache Airflow para pipeline ETL de ventas"
LABEL version="1.0"

# Cambiar a usuario root para instalar dependencias del sistema
USER root

# Instalar dependencias del sistema si son necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear directorios necesarios
RUN mkdir -p /opt/airflow/data/input \
    /opt/airflow/data/output \
    /opt/airflow/logs \
    /opt/airflow/plugins

# Cambiar permisos
RUN chown -R airflow:root /opt/airflow

# Volver al usuario airflow
USER airflow

# Copiar requirements.txt
COPY --chown=airflow:root requirements.txt /opt/airflow/requirements.txt

# Instalar dependencias de Python
RUN pip install --no-cache-dir --user -r /opt/airflow/requirements.txt

# Copiar el código del proyecto
COPY --chown=airflow:root dags /opt/airflow/dags
COPY --chown=airflow:root scripts /opt/airflow/scripts
COPY --chown=airflow:root config /opt/airflow/config
COPY --chown=airflow:root .env /opt/airflow/.env

# Establecer variables de entorno
ENV AIRFLOW_HOME=/opt/airflow
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"

# Exponer puerto del webserver
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD airflow jobs check --job-type SchedulerJob --hostname "$${HOSTNAME}" || exit 1

# Comando por defecto (será sobrescrito por docker-compose)
CMD ["airflow", "webserver"]
