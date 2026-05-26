def validate_utility(record_data):
    if record_data.get("source_type") != "utility":
        return []

    reasons = []
    start_date = record_data.get("start_date")
    end_date = record_data.get("end_date")
    if start_date and end_date and end_date < start_date:
        reasons.append("Billing end date is before billing start date")
    if not record_data.get("metadata", {}).get("meter_id"):
        reasons.append("Missing meter identifier")
    return reasons

