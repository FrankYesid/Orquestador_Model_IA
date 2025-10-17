"""
Tests para el módulo de transformación de datos.
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.transform_data import (
    clean_data,
    transform_data,
    aggregate_data
)


class TestTransformData:
    """Tests para el módulo de transformación."""
    
    @pytest.fixture
    def sample_dataframe(self):
        """Crea un DataFrame de ejemplo para tests."""
        return pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'fecha': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']),
            'producto': ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Webcam'],
            'categoria': ['Computadoras', 'Accesorios', 'Accesorios', 'Computadoras', 'Accesorios'],
            'region': ['Norte', 'Sur', 'Este', 'Oeste', 'Centro'],
            'cantidad': [1, 2, 3, 1, 2],
            'precio_unitario': [1000.0, 25.0, 75.0, 500.0, 100.0],
            'descuento': [0.1, 0.0, np.nan, 0.05, 0.0],
            'total_venta': [900.0, 50.0, 225.0, 475.0, 200.0]
        })
    
    def test_clean_data_removes_nulls(self, sample_dataframe):
        """Test que clean_data maneja valores nulos correctamente."""
        df_clean = clean_data(sample_dataframe)
        
        # Verificar que los descuentos nulos fueron rellenados con 0
        assert df_clean['descuento'].isnull().sum() == 0
    
    def test_clean_data_removes_duplicates(self):
        """Test que clean_data elimina duplicados."""
        df = pd.DataFrame({
            'id': [1, 1, 2],
            'fecha': pd.to_datetime(['2023-01-01', '2023-01-01', '2023-01-02']),
            'producto': ['Laptop', 'Laptop', 'Mouse'],
            'categoria': ['Computadoras', 'Computadoras', 'Accesorios'],
            'region': ['Norte', 'Norte', 'Sur'],
            'cantidad': [1, 1, 2],
            'precio_unitario': [1000.0, 1000.0, 25.0],
            'descuento': [0.1, 0.1, 0.0],
            'total_venta': [900.0, 900.0, 50.0]
        })
        
        df_clean = clean_data(df)
        
        # Debe haber eliminado 1 duplicado
        assert len(df_clean) < len(df)
    
    def test_clean_data_removes_invalid_quantities(self):
        """Test que clean_data elimina cantidades inválidas."""
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'fecha': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']),
            'producto': ['Laptop', 'Mouse', 'Teclado'],
            'categoria': ['Computadoras', 'Accesorios', 'Accesorios'],
            'region': ['Norte', 'Sur', 'Este'],
            'cantidad': [1, 0, -1],  # Cantidades inválidas
            'precio_unitario': [1000.0, 25.0, 75.0],
            'descuento': [0.1, 0.0, 0.0],
            'total_venta': [900.0, 50.0, 225.0]
        })
        
        df_clean = clean_data(df)
        
        # Solo debe quedar el registro con cantidad válida
        assert len(df_clean) == 1
        assert df_clean['cantidad'].iloc[0] == 1
    
    def test_transform_data_adds_date_components(self, sample_dataframe):
        """Test que transform_data agrega componentes de fecha."""
        df_transformed = transform_data(sample_dataframe)
        
        # Verificar que se agregaron las columnas de fecha
        assert 'año' in df_transformed.columns
        assert 'mes' in df_transformed.columns
        assert 'dia' in df_transformed.columns
        assert 'trimestre' in df_transformed.columns
    
    def test_transform_data_adds_calculated_metrics(self, sample_dataframe):
        """Test que transform_data calcula métricas derivadas."""
        df_transformed = transform_data(sample_dataframe)
        
        # Verificar que se agregaron métricas calculadas
        assert 'ingreso_bruto' in df_transformed.columns
        assert 'descuento_total' in df_transformed.columns
        assert 'margen' in df_transformed.columns
    
    def test_transform_data_adds_categories(self, sample_dataframe):
        """Test que transform_data categoriza ventas."""
        df_transformed = transform_data(sample_dataframe)
        
        # Verificar que se agregó la categorización
        assert 'categoria_venta' in df_transformed.columns
        
        # Verificar que las categorías son válidas
        valid_categories = ['Pequeña', 'Mediana', 'Grande', 'Premium']
        assert all(cat in valid_categories for cat in df_transformed['categoria_venta'].unique())
    
    def test_aggregate_data_reduces_rows(self, sample_dataframe):
        """Test que aggregate_data reduce el número de filas."""
        df_clean = clean_data(sample_dataframe)
        df_aggregated = aggregate_data(df_clean)
        
        # El DataFrame agregado debe tener igual o menos filas
        assert len(df_aggregated) <= len(df_clean)
    
    def test_aggregate_data_has_correct_columns(self, sample_dataframe):
        """Test que aggregate_data tiene las columnas correctas."""
        df_clean = clean_data(sample_dataframe)
        df_aggregated = aggregate_data(df_clean)
        
        # Verificar columnas esperadas
        expected_columns = [
            'fecha', 'producto', 'categoria', 'region',
            'cantidad_total', 'precio_promedio', 'descuento_promedio',
            'total_venta', 'num_transacciones'
        ]
        
        for col in expected_columns:
            assert col in df_aggregated.columns
