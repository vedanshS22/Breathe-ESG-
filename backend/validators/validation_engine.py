from validators.quantity_validator import validate_quantity
from validators.travel_validator import validate_travel
from validators.utility_validator import validate_utility


def evaluate_record(record_data):
    reasons = []
    reasons.extend(record_data.get("metadata", {}).get("normalization_warnings", []))
    reasons.extend(validate_quantity(record_data))
    reasons.extend(validate_utility(record_data))
    reasons.extend(validate_travel(record_data))

    unique_reasons = []
    for reason in reasons:
        if reason and reason not in unique_reasons:
            unique_reasons.append(reason)

    return {
        "is_suspicious": bool(unique_reasons),
        "suspicious_reason": "; ".join(unique_reasons),
    }

