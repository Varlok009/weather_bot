def lon_validator(lon: str):
    """Выполняет простую валидацию полученного значения на соответствие значению долготы"""

    if lon.replace('.', '').isdigit() and -180 <= float(lon) <= 180:
        return True
    else: return False