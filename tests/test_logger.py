from src.utils.logger import get_logger


logger = get_logger("test")

logger.info("Logger is working")
logger.warning("This is a warning")
logger.error("This is an error")
