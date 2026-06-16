import time
from langchain.tools import tool


@tool
def get_current_time() -> int:
    """
    Used to get the current time in seconds from epoch
    """
    print("[TOOL_CALLED] get_current_time")
    return int(time.time())
