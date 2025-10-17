"""
Tests para el módulo de carga de datos.
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

from scripts.load_data import (
    validate_data_before_load,
    prepare_data_for_load
)


class TestLoadData:
    """Tests para el módulo de carga."""
    
    @pytest.fixture
    def sample_transformed_dataframe(self):
        """Crea un DataFrame transformado de ejemplo para tests."""
        return pd.DataFrame({
            'fecha': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'producto': ['Laptop', 'Mouse', 'Teclado'],
            'categoria': ['Computadoras', 'Accesorios', 'Accesorios'],
            'region': ['Norte', 'Sur', 'Este'],
            'cantidad_total': [10, 20, 30],
            'precio_promedio': [1000.0, 25.0, 75.0],
            'descuento_promedio': [0.1, 0.05, 0.0],
            'total_venta': [9000.0, 475.0, 2250.0],
            'num_transacciones': [5, 10, 15]
        })
    
    def test_validate_data_before_load_valid(self, sample_transformed_dataframe):
        """Test que valida datos correctos antes de la carga."""
        result = validate_data_before_load(sample_transformed_dataframe)
        assert result is True
    
    def test_validate_data_before_load_empty(self):
        """Test que detecta DataFrame vacío."""
        df = pd.DataFrame()
        result = validate_data_before_load(df)
        assert result is False
    
    def test_validate_data_before_load_missing_columns(self):
        """Test que detecta columnas faltantes."""
        df = pd.DataFrame({
            'fecha': ['2023-01-01', '2023-01-02'],
            'producto': ['Laptop', 'Mouse']
        })
        result = validate_data_before_load(df)
        assert result is False
    
    def test_validate_data_before_load_null_values(self):
        """Test que detecta valores nulos en columnas críticas."""
        df = pd.DataFrame({
            'fecha': [None, '2023-01-02', '2023-01-03'],
            'producto': ['Laptop', 'Mouse', 'Teclado'],
            'categoria': ['Computadoras', 'Accesorios', 'Accesorios'],
            'region': ['Norte', 'Sur', 'Este'],
            'cantidad_total': [10, 20, 30],
            'precio_promedio': [1000.0, 25.0, 75.0],
            'descuento_promedio': [0.1, 0.05, 0.0],
            'total_venta': [9000.0, 475.0, 2250.0],
            'num_transacciones': [5, 10, 15]
        })
        result = validate_data_before_load(df)
        assert result is False
    
    def test_validate_data_before_load_negative_values(self):
        """Test que detecta valores negativos."""
        df = pd.DataFrame({
            'fecha': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'producto': ['Laptop', 'Mouse', 'Teclado'],
            'categoria': ['Computadoras', 'Accesorios', 'Accesorios'],
            'region': ['Norte', 'Sur', 'Este'],
            'cantidad_total': [10, -20, 30],  # Valor negativo
            'precio_promedio': [1000.0, 25.0, 75.0],
            'descuento_promedio': [0.1, 0.05, 0.0],
            'total_venta': [9000.0, 475.0, 2250.0],
            'num_transacciones': [5, 10, 15]
        })
        result = validate_data_before_load(df)
        assert result is False
    
    def test_prepare_data_for_load_converts_dates(self, sample_transformed_dataframe):
        """Test que prepare_data_for_load convierte fechas correctamente."""
        df_prepared = prepare_data_for_load(sample_transformed_dataframe)
        
        # Verificar que las fechas son strings
        assert df_prepared['fecha'].dtype == object
        assert all(isinstance(date, str) for date in df_prepared['fecha'])
    
    def test_prepare_data_for_load_sorts_by_date(self, sample_transformed_dataframe):
        """Test que prepare_data_for_load ordena por fecha."""
        # Desordenar el DataFrame
        df_unsorted = sample_transformed_dataframe.sample(frac=1).reset_index(drop=True)
        
        df_prepared = prepare_data_for_load(df_unsorted)
        
        # Verificar que está ordenado
        dates = pd.to_datetime(df_prepared['fecha'])
        assert all(dates[i] <= dates[i+1] for i in range(len(dates)-1))
    
    def test_prepare_data_for_load_numeric_types(self, sample_transformed_dataframe):
        """Test que prepare_data_for_load asegura tipos numéricos."""
        df_prepared = prepare_data_for_load(sample_transformed_dataframe)
        
        # Verificar tipos numéricos
        numeric_columns = ['cantidad_total', 'precio_promedio', 'total_venta', 'num_transacciones']
        for col in numeric_columns:
            assert pd.api.types.is_numeric_dtype(df_prepared[col])
