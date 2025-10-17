"""
Tests para el módulo de extracción de datos.
"""

import pytest
import pandas as pd
import sqlite3
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.extract_data import (
    extract_data_from_db,
    validate_extracted_data,
    save_extracted_data
)


class TestExtractData:
    """Tests para el módulo de extracción."""
    
    @pytest.fixture
    def sample_dataframe(self):
        """Crea un DataFrame de ejemplo para tests."""
        return pd.DataFrame({
            'id': [1, 2, 3],
            'fecha': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'producto': ['Laptop', 'Mouse', 'Teclado'],
            'cantidad': [1, 2, 3],
            'precio_unitario': [1000.0, 25.0, 75.0],
            'total_venta': [1000.0, 50.0, 225.0]
        })
    
    def test_validate_extracted_data_valid(self, sample_dataframe):
        """Test que valida datos correctos."""
        result = validate_extracted_data(sample_dataframe)
        assert result is True
    
    def test_validate_extracted_data_empty(self):
        """Test que detecta DataFrame vacío."""
        df = pd.DataFrame()
        result = validate_extracted_data(df)
        assert result is False
    
    def test_validate_extracted_data_missing_columns(self):
        """Test que detecta columnas faltantes."""
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'fecha': ['2023-01-01', '2023-01-02', '2023-01-03']
        })
        result = validate_extracted_data(df)
        assert result is False
    
    def test_save_extracted_data(self, sample_dataframe, tmp_path):
        """Test que guarda datos correctamente."""
        output_path = str(tmp_path)
        filename = 'test_extracted.csv'
        
        save_extracted_data(sample_dataframe, output_path, filename)
        
        # Verificar que el archivo existe
        file_path = os.path.join(output_path, filename)
        assert os.path.exists(file_path)
        
        # Verificar contenido
        df_loaded = pd.read_csv(file_path)
        assert len(df_loaded) == len(sample_dataframe)
        assert list(df_loaded.columns) == list(sample_dataframe.columns)
