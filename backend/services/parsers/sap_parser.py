from services.parsers.base import BaseCsvParser


class SapFlatFileParser(BaseCsvParser):
    required_alias_groups = {
        "quantity": ["Qty", "Quantity", "Menge", "MENGE", "Order Quantity"],
        "unit": ["UOM", "Unit", "MEINS", "Einheit"],
    }

