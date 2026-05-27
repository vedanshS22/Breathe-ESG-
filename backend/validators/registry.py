from validators.sap_validator import validate_sap
from validators.travel_validator import validate_travel
from validators.utility_validator import validate_utility


SOURCE_VALIDATORS = {
    "sap": validate_sap,
    "utility": validate_utility,
    "travel": validate_travel,
}


def validate_source_record(record_data):
    validator = SOURCE_VALIDATORS.get(record_data.get("source_type"))
    if not validator:
        return []
    return validator(record_data)
