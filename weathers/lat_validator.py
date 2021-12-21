def lat_validator(lon: str):
    """Выполняет простую валидацию полученного значения на соответствие значению шиторы"""

    if lon.replace('.', '').isdigit() and -90 <= float(lon) <= 90:
        return True
    else: return False