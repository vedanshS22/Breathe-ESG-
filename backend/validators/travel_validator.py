def validate_travel(record_data):
    if record_data.get("source_type") != "travel":
        return []

    reasons = []
    metadata = record_data.get("metadata", {})
    origin = metadata.get("origin_airport")
    destination = metadata.get("destination_airport")
    category = record_data.get("category", "")

    if "Flight" in category:
        if origin and len(origin) != 3:
            reasons.append("Invalid origin airport code")
        if destination and len(destination) != 3:
            reasons.append("Invalid destination airport code")
        if not origin or not destination:
            reasons.append("Missing flight airport pair")

    return reasons

