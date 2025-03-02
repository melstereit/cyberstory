# cyberstory/debug.py
import time
import os
from typing import Any, Dict, Optional

def debug_log(message: str, data: Optional[Any] = None) -> None:
    """
    Logs debug information to a file with timestamps.
    
    Args:
        message: The message to log
        data: Optional data to include in the log
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(log_dir, f"debug_{time.strftime('%Y%m%d')}.log")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
        if data is not None:
            if isinstance(data, dict):
                for key, value in data.items():
                    f.write(f"  {key}: {value}\n")
            else:
                f.write(f"  {data}\n")
        f.write("\n")