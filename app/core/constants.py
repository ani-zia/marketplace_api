from pathlib import Path

BASE_DIR = Path(__file__).parents[2]
LOG_MSG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
LOG_DT_FORMAT = "%d.%m.%Y %H:%M:%S"
PAGINATION_DEFAULT = 5
PASSWORD_MIN_LENGHT = 3
