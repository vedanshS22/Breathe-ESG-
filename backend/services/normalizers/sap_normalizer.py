from services.normalizers.common import (
    first_present,
    normalize_unit,
    parse_number,
    parse_operational_date,
)


class SapNormalizer:
    source_type = "sap"

    def normalize(self, row):
        warnings = []

        quantity = parse_number(
            first_present(row, ["Qty", "Quantity", "Menge", "MENGE", "Order Quantity"])
        )
        if quantity is None:
            warnings.append("Missing or invalid quantity")

        unit, unit_warning = normalize_unit(first_present(row, ["UOM", "Unit", "MEINS", "Einheit"]))
        if unit_warning:
            warnings.append(unit_warning)

        start_date, date_warning = parse_operational_date(
            first_present(row, ["Posting Date", "Buchungsdatum", "BUDAT", "Date"])
        )
        if date_warning:
            warnings.append(date_warning)

        fuel_type = first_present(
            row,
            ["Fuel_Type", "Fuel Type", "Material Description", "Kraftstoff", "Kraftstoffart"],
            "fuel",
        )
        plant = first_present(row, ["Plant", "Werk", "WERKS"], "")
        document = first_present(row, ["Document Number", "Material Document", "MBLNR", "PO Number"], "")

        return {
            "source_type": self.source_type,
            "source_reference": str(document or plant or ""),
            "scope": "Scope 1",
            "category": "Fuel",
            "quantity": quantity,
            "normalized_unit": unit,
            "start_date": start_date,
            "end_date": start_date,
            "raw_data": row,
            "metadata": {
                "fuel_type": fuel_type,
                "plant_code": plant,
                "document_number": document,
                "normalization_warnings": warnings,
            },
        }

