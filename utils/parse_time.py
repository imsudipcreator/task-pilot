def parse_time_str(time_str: str) -> int:
    """
    Parse time string to seconds
    Examples:
    - 1s -> 1 second
    - 1m -> 1 minute
    - 1h -> 1 hour
    - 1d -> 1 day
    """
    value = int(time_str[:-1])
    unit = time_str[-1].lower()

    multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400}

    if unit not in multipliers:
        raise ValueError("Invalid time unit. Use s, m, h, or d")

    return value * multipliers[unit]
