import logging

LOGGER = logging.getLogger(__name__)

# configure logging
def configure_logging():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
