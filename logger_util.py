# logger_util.py 统一日志工具
import logging
import os
from datetime import datetime

LOG_FOLDER = "logs"
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

log_filename = os.path.join(LOG_FOLDER, f"job_project_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
log_format = logging.Formatter("%(asctime)s | %(levelname)s | %(module)s | %(message)s")

file_handler = logging.FileHandler(log_filename, encoding="utf-8")
file_handler.setFormatter(log_format)
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)

logger = logging.getLogger("job_market_log")
logger.setLevel(logging.INFO)
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

if __name__ == "__main__":
    logger.info("日志模块初始化完成")
