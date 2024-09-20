def convert(value, to_unit):
    if value.endswith("in") and to_unit == "cm":
        inches = float(value[:-2])
        return inches * 2.54
    return None