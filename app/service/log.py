from datetime import datetime
from app.common.constants import LogPy


def log(message: str, source: str, doPrint: bool, error: Exception = None):
    # 构造时间戳
    timestamp = datetime.now().strftime(LogPy.TIME_STAMP_FORMAT)

    # 构造最终消息
    if error is None:
        log_message = LogPy.LOG_FORMAT.format(timestamp=timestamp, source=source, message=message)
    else:
        log_message = LogPy.LOG_FORMAT_WITH_ERROR.format(
            timestamp=timestamp, source=source, message=message, error=str(error))

    # 控制台输出
    if doPrint:
        print(log_message)
