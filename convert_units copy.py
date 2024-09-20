def convert(value, to_unit):
    if isinstance(value, str) and value.endswith("in") and to_unit == "cm":
        inches = float(value[:-2])
        return round(inches * 2.54, 2)
    elif isinstance(value, str) and value.endswith("cm") and to_unit == "in":
        centimeters = float(value[:-2])
        return round(centimeters / 2.54, 2)
    elif isinstance(value, str) and value.endswith("yd") and to_unit == "m":
        yards = float(value[:-2])
        return round(yards * 0.9144, 3)  # Changed precision to 3 decimal places
    elif isinstance(value, str) and value.endswith("m") and to_unit == "yd":
        meters = float(value[:-1])
        return round(meters / 0.9144, 4)
    return None