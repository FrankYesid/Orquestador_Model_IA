"""
Configuración de la base de datos para el proyecto ETL.
Este módulo maneja la conexión y configuración de SQLite.
"""

import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()


class DatabaseConfig:
    """
    Clase para manejar la configuración de la base de datos.
    Proporciona métodos para conectar y gestionar la base de datos SQLite.
    """
    
    def __init__(self):
        """Inicializa la configuración de la base de datos."""
        self.db_path = os.getenv('DB_PATH', 'data/database.db')
        self.db_type = os.getenv('DB_TYPE', 'sqlite')
        self.table_source = os.getenv('DB_TABLE_SOURCE', 'sales_data')
        self.table_target = os.getenv('DB_TABLE_TARGET', 'sales_transformed')
        
        # Crear directorio si no existe
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Configuración de BD inicializada: {self.db_path}")
    
    def get_connection(self):
        """
        Crea y retorna una conexión a la base de datos SQLite.
        
        Returns:
            sqlite3.Connection: Objeto de conexión a la base de datos
        """
        try:
            conn = sqlite3.connect(self.db_path)
            logger.info(f"Conexión establecida a: {self.db_path}")
            return conn
        except sqlite3.Error as e:
            logger.error(f"Error al conectar a la base de datos: {e}")
            raise
    
    def close_connection(self, conn):
        """
        Cierra la conexión a la base de datos.
        
        Args:
            conn: Objeto de conexión a cerrar
        """
        if conn:
            conn.close()
            logger.info("Conexión cerrada correctamente")
    
    def execute_query(self, query, params=None, fetch=False):
        """
        Ejecuta una consulta SQL en la base de datos.
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple, optional): Parámetros para la consulta
            fetch (bool): Si True, retorna los resultados
            
        Returns:
            list: Resultados de la consulta si fetch=True
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                results = cursor.fetchall()
                return results
            else:
                conn.commit()
                logger.info("Consulta ejecutada exitosamente")
        except sqlite3.Error as e:
            logger.error(f"Error ejecutando consulta: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
            self.close_connection(conn)
    
    def table_exists(self, table_name):
        """
        Verifica si una tabla existe en la base de datos.
        
        Args:
            table_name (str): Nombre de la tabla a verificar
            
        Returns:
            bool: True si la tabla existe, False en caso contrario
        """
        query = """
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """
        result = self.execute_query(query, (table_name,), fetch=True)
        return len(result) > 0
    
    def get_table_info(self, table_name):
        """
        Obtiene información sobre las columnas de una tabla.
        
        Args:
            table_name (str): Nombre de la tabla
            
        Returns:
            list: Información de las columnas
        """
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query, fetch=True)


# Instancia global de configuración
db_config = DatabaseConfig()
