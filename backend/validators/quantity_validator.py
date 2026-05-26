def validate_quantity(record_data):
    reasons = []
    quantity = record_data.get("quantity")
    unit = record_data.get("normalized_unit")

    if quantity is None:
        reasons.append("Missing quantity")
        return reasons

    if quantity < 0:
        reasons.append("Negative quantity")

    if unit == "kwh" and quantity > 10_000_000:
        reasons.append("Electricity usage is unusually high")
    elif unit == "liters" and quantity > 1_000_000:
        reasons.append("Fuel volume is unusually high")
    elif unit in {"km", "miles"} and quantity > 50_000:
        reasons.append("Travel distance is unusually high")
    elif unit == "nights" and quantity > 60:
        reasons.append("Hotel stay length is unusually high")

    return reasons

