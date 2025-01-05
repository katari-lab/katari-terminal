from src.components.TerminalComponent import TerminalComponent
import logging
import configparser
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s:%(lineno)d - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

LOGGER = logging.getLogger(__name__)

def load_init():
    LOGGER.info("Loading environment variables from startup.ini")
    if not os.path.exists('startup.ini'):
        raise ValueError("startup.ini file not found")
    config = configparser.ConfigParser()
    config.read('startup.ini')
    
    if 'DEFAULT' in config:
        for key, value in config['DEFAULT'].items():
            key = key.upper()
            os.environ[key] = value
            print(f"Setting {key}")

if __name__ == "__main__":
    LOGGER.info("Starting the application")
    load_init()
    component = TerminalComponent()
    component.run()
