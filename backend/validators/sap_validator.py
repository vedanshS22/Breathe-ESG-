def validate_sap(record_data):
    if record_data.get("source_type") != "sap":
        return []

    reasons = []
    metadata = record_data.get("metadata", {})
    if not metadata.get("plant_code"):
        reasons.append("Missing SAP plant code")
    if not metadata.get("document_number"):
        reasons.append("Missing SAP material document reference")
    return reasons
