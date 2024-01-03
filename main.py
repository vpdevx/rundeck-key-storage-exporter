from exporter import StorageExporter
from logging_config import logger
import os

def main():
    """Main function."""
    
    DEFAULT_DB_PATH = ""
    DEFAULT_DB_USER = ""
    DEFAULT_DB_PASSWORD = ""
    DEFAULT_RUNDECK_URL = "http://127.0.0.1:4440"
    DEFAULT_RUNDECK_TOKEN = ""
    
    db_path = os.getenv("DB_PATH", DEFAULT_DB_PATH)
    db_user = os.getenv("DB_USER", DEFAULT_DB_USER)
    db_password = os.getenv("DB_PASSWORD", DEFAULT_DB_PASSWORD)
    rundeck_url = os.getenv("RUNDECK_URL", DEFAULT_RUNDECK_URL)
    rundeck_token = os.getenv("RUNDECK_TOKEN", DEFAULT_RUNDECK_TOKEN)
    
    optional_vars = ["DB_USER", "DB_PASSWORD", "RUNDECK_URL"]
    required_vars = ["DB_PATH", "RUNDECK_TOKEN"]

    for var in required_vars:
        if not os.getenv(var):
            logger.error("Variável de ambiente não definida: " + var)
            exit(1)
            
    for var in optional_vars:
        if not os.getenv(var):
            logger.warning("Variável de ambiente " + var + " não definida. Utilizando valor padrão.")
    
    exporter = StorageExporter(rundeck_url, rundeck_token, db_path, db_user, db_password)
    exporter.connect() 
    exporter.get_key_storage()
    exporter.close_connection()

if __name__ == "__main__":
    main()