from src.components.TerminalComponent import TerminalComponent
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s:%(lineno)d - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    LOGGER.info("Starting the application")
    component = TerminalComponent()
    component.run()
