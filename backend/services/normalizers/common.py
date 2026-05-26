from datetime import date, datetime
from math import asin, cos, radians, sin, sqrt

try:
    from dateutil import parser as date_parser
except ImportError:  # pragma: no cover - local fallback for constrained runtimes
    date_parser = None

from services.parsers.base import normalize_header


UNIT_MAPPINGS = {
    "l": "liters",
    "ltr": "liters",
    "liter": "liters",
    "liters": "liters",
    "litre": "liters",
    "litres": "liters",
    "gal": "gallons",
    "gallon": "gallons",
    "gallons": "gallons",
    "kwh": "kwh",
    "kw h": "kwh",
    "kilowatt hour": "kwh",
    "kilowatt hours": "kwh",
    "mwh": "mwh",
    "km": "km",
    "kilometer": "km",
    "kilometers": "km",
    "mi": "miles",
    "mile": "miles",
    "miles": "miles",
    "night": "nights",
    "nights": "nights",
}

AIRPORT_COORDINATES = {
    "DEL": (28.5562, 77.1),
    "LHR": (51.47, -0.4543),
    "JFK": (40.6413, -73.7781),
    "SFO": (37.6213, -122.379),
    "BOM": (19.0896, 72.8656),
    "BLR": (13.1986, 77.7066),
    "DXB": (25.2532, 55.3657),
    "SIN": (1.3644, 103.9915),
}


def first_present(row, aliases, default=None):
    normalized = {normalize_header(key): value for key, value in row.items()}
    for alias in aliases:
        value = normalized.get(normalize_header(alias))
        if value not in (None, ""):
            return value
    return default


def parse_number(value):
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = str(value).strip().replace(",", "")
    cleaned = cleaned.replace("km", "").replace("kWh", "").replace("KWH", "")
    cleaned = cleaned.replace("L", "").replace("ltr", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


def normalize_unit(value):
    if value in (None, ""):
        return "", "Missing unit"
    key = normalize_header(value)
    normalized = UNIT_MAPPINGS.get(key)
    if normalized:
        return normalized, ""
    return key, f"Unknown unit: {value}"


def parse_operational_date(value):
    if value in (None, ""):
        return None, "Missing date"
    if isinstance(value, date) and not isinstance(value, datetime):
        return value, ""
    if isinstance(value, datetime):
        return value.date(), ""

    text = str(value).strip()
    formats = (
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d.%m.%Y",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%m-%d-%Y",
        "%b %d %Y",
        "%B %d %Y",
    )
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).date(), ""
        except ValueError:
            continue

    if date_parser:
        try:
            return date_parser.parse(text, dayfirst=True).date(), ""
        except (ValueError, TypeError, OverflowError):
            pass
    return None, f"Invalid date: {value}"


def split_reasons(reasons):
    return "; ".join(reason for reason in reasons if reason)


def airport_distance_km(origin, destination):
    origin = str(origin or "").strip().upper()
    destination = str(destination or "").strip().upper()
    if origin not in AIRPORT_COORDINATES or destination not in AIRPORT_COORDINATES:
        return None

    lat1, lon1 = AIRPORT_COORDINATES[origin]
    lat2, lon2 = AIRPORT_COORDINATES[destination]
    radius_km = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return round(radius_km * c, 1)

