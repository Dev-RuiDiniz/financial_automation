import logging
from pathlib import Path

def get_logger(name="financial"):
    log_path = Path("data/reports/logs.txt")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(name)
