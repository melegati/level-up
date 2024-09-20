def convert(value, to_unit):
    if isinstance(value, str) and value.endswith("in") and to_unit == "cm":
        inches = float(value[:-2])
        return inches * 2.54, 2
    elif isinstance(value, str) and value.endswith("cm") and to_unit == "in":
        centimeters = float(value[:-2])
        return centimeters / 2.54, 2
    elif isinstance(value, str) and value.endswith("yd") and to_unit == "m":
        yards = float(value[:-2])
        return yards * 0.9144, 2
    elif isinstance(value, str) and value.endswith("m") and to_unit == "yd":
        meters = float(value[:-1])
        return meters / 0.9144, 2
    return None