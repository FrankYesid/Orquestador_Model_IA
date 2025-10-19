# Makefile para el proyecto de Orquestación ETL con Apache Airflow
# Facilita la ejecución de comandos comunes

.PHONY: help install setup-db start-airflow stop-airflow test lint format clean docker-up docker-down

# Variables
PYTHON := python
PIP := pip
AIRFLOW := airflow
DOCKER_COMPOSE := docker-compose

# Colores para output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Muestra esta ayuda
	@echo "$(GREEN)Comandos disponibles:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Instala las dependencias del proyecto
	@echo "$(GREEN)Instalando dependencias...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Dependencias instaladas$(NC)"

install-dev: ## Instala dependencias de desarrollo
	@echo "$(GREEN)Instalando dependencias de desarrollo...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov black flake8 isort mypy
	@echo "$(GREEN)✓ Dependencias de desarrollo instaladas$(NC)"

setup-db: ## Crea la base de datos dummy
	@echo "$(GREEN)Creando base de datos dummy...$(NC)"
	$(PYTHON) scripts/create_dummy_db.py
	@echo "$(GREEN)✓ Base de datos creada$(NC)"

init-airflow: ## Inicializa Airflow
	@echo "$(GREEN)Inicializando Airflow...$(NC)"
	$(AIRFLOW) db init
	@echo "$(GREEN)Creando usuario admin...$(NC)"
	$(AIRFLOW) users create \
		--username admin \
		--firstname Admin \
		--lastname User \
		--role Admin \
		--email admin@example.com \
		--password admin
	@echo "$(GREEN)✓ Airflow inicializado$(NC)"

start-airflow: ## Inicia Airflow (webserver y scheduler)
	@echo "$(GREEN)Iniciando Airflow...$(NC)"
	@echo "$(YELLOW)Webserver: http://localhost:8080$(NC)"
	@echo "$(YELLOW)Usuario: admin | Contraseña: admin$(NC)"
	$(AIRFLOW) scheduler & $(AIRFLOW) webserver

stop-airflow: ## Detiene Airflow
	@echo "$(RED)Deteniendo Airflow...$(NC)"
	pkill -f "airflow scheduler" || true
	pkill -f "airflow webserver" || true
	@echo "$(GREEN)✓ Airflow detenido$(NC)"

test: ## Ejecuta los tests
	@echo "$(GREEN)Ejecutando tests...$(NC)"
	pytest tests/ -v --cov=scripts --cov-report=term-missing

test-coverage: ## Ejecuta tests con reporte de cobertura HTML
	@echo "$(GREEN)Ejecutando tests con cobertura...$(NC)"
	pytest tests/ -v --cov=scripts --cov-report=html
	@echo "$(GREEN)✓ Reporte generado en htmlcov/index.html$(NC)"

lint: ## Verifica el estilo del código
	@echo "$(GREEN)Verificando estilo del código...$(NC)"
	flake8 scripts/ dags/ config/ --max-line-length=120
	@echo "$(GREEN)✓ Código verificado$(NC)"

format: ## Formatea el código
	@echo "$(GREEN)Formateando código...$(NC)"
	black scripts/ dags/ config/
	isort scripts/ dags/ config/
	@echo "$(GREEN)✓ Código formateado$(NC)"

type-check: ## Verifica tipos con mypy
	@echo "$(GREEN)Verificando tipos...$(NC)"
	mypy scripts/ dags/ config/ --ignore-missing-imports
	@echo "$(GREEN)✓ Tipos verificados$(NC)"

clean: ## Limpia archivos generados
	@echo "$(RED)Limpiando archivos generados...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov/ .mypy_cache/
	rm -rf data/output/*.csv
	@echo "$(GREEN)✓ Archivos limpiados$(NC)"

clean-db: ## Elimina la base de datos
	@echo "$(RED)Eliminando base de datos...$(NC)"
	rm -f data/database.db
	@echo "$(GREEN)✓ Base de datos eliminada$(NC)"

docker-up: ## Inicia servicios con Docker Compose
	@echo "$(GREEN)Iniciando servicios con Docker...$(NC)"
	cd docker && $(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)✓ Servicios iniciados$(NC)"
	@echo "$(YELLOW)Webserver: http://localhost:8080$(NC)"
	@echo "$(YELLOW)Usuario: airflow | Contraseña: airflow$(NC)"

docker-down: ## Detiene servicios de Docker
	@echo "$(RED)Deteniendo servicios de Docker...$(NC)"
	cd docker && $(DOCKER_COMPOSE) down
	@echo "$(GREEN)✓ Servicios detenidos$(NC)"

docker-logs: ## Muestra logs de Docker
	cd docker && $(DOCKER_COMPOSE) logs -f

docker-clean: ## Elimina contenedores y volúmenes de Docker
	@echo "$(RED)Eliminando contenedores y volúmenes...$(NC)"
	cd docker && $(DOCKER_COMPOSE) down -v
	@echo "$(GREEN)✓ Contenedores y volúmenes eliminados$(NC)"

run-extract: ## Ejecuta solo el script de extracción
	@echo "$(GREEN)Ejecutando extracción...$(NC)"
	$(PYTHON) scripts/extract_data.py

run-transform: ## Ejecuta solo el script de transformación
	@echo "$(GREEN)Ejecutando transformación...$(NC)"
	$(PYTHON) scripts/transform_data.py

run-load: ## Ejecuta solo el script de carga
	@echo "$(GREEN)Ejecutando carga...$(NC)"
	$(PYTHON) scripts/load_data.py

run-pipeline: ## Ejecuta el pipeline completo (extract, transform, load)
	@echo "$(GREEN)Ejecutando pipeline completo...$(NC)"
	$(PYTHON) scripts/extract_data.py
	$(PYTHON) scripts/transform_data.py
	$(PYTHON) scripts/load_data.py
	@echo "$(GREEN)✓ Pipeline completado$(NC)"

setup: install setup-db init-airflow ## Configuración completa del proyecto
	@echo "$(GREEN)✓ Proyecto configurado completamente$(NC)"
	@echo "$(YELLOW)Ejecuta 'make start-airflow' para iniciar Airflow$(NC)"

.DEFAULT_GOAL := help
