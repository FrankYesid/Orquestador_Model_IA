"""
Setup script para el proyecto de Orquestación ETL con Apache Airflow.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Leer el README para la descripción larga
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Leer requirements
requirements = (this_directory / "requirements.txt").read_text(encoding='utf-8').splitlines()

setup(
    name="airflow-etl-pipeline",
    version="1.0.0",
    author="Proyecto ETL Team",
    author_email="admin@example.com",
    description="Pipeline ETL educativo con Apache Airflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/Orquestador_Model_IA",
    project_urls={
        "Bug Tracker": "https://github.com/tu-usuario/Orquestador_Model_IA/issues",
        "Documentation": "https://github.com/tu-usuario/Orquestador_Model_IA/blob/main/README.md",
        "Source Code": "https://github.com/tu-usuario/Orquestador_Model_IA",
    },
    packages=find_packages(exclude=["tests", "tests.*", "docs", "docs.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.7.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "create-dummy-db=scripts.create_dummy_db:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="airflow etl data-pipeline data-engineering educational",
)
