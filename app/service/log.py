from datetime import datetime

def log(message: str, error: Exception, source: str, doPrint: bool):
    # 构造时间戳
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 构造最终消息
    log_message = f"[{timestamp}] [{source}] {message}"
    if error:
        log_message += f" | ERROR: {str(error)}"

    # 控制台输出
    if doPrint:
        print(log_message)