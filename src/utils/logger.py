import logging
import os


# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)


def get_logger(name):
    """
    Create and return a configured logger.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # Write logs to file
    file_handler = logging.FileHandler(
        "logs/pipeline.log"
    )
    file_handler.setFormatter(formatter)

    # Also display logs in terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger