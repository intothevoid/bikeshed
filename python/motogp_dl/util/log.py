import sys
import logging

# setup logging
logging.basicConfig(
    filename=f"motogp_dl.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# add console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logging.getLogger("").addHandler(console_handler)

LOGGER = logging.getLogger(__name__)
