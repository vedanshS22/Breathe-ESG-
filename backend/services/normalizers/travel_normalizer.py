from services.normalizers.common import (
    airport_distance_km,
    first_present,
    normalize_unit,
    parse_number,
    parse_operational_date,
)


class TravelNormalizer:
    source_type = "travel"

    def normalize(self, row):
        warnings = []

        category_value = str(
            first_present(row, ["Category", "Trip Type", "Travel Type", "Expense Type"], "")
        ).lower()
        start_date, date_warning = parse_operational_date(
            first_present(row, ["Trip Date", "Booking Date", "Transaction Date", "Start Date"])
        )
        if date_warning:
            warnings.append(date_warning)

        origin = first_present(row, ["From Airport", "from_airport", "Origin", "Origin Airport"], "")
        destination = first_present(
            row,
            ["To Airport", "to_airport", "Destination", "Destination Airport"],
            "",
        )

        if "hotel" in category_value:
            quantity = parse_number(first_present(row, ["Nights", "night_count", "Quantity"]))
            unit, unit_warning = normalize_unit(first_present(row, ["Unit"], "nights"))
            category = "Business Travel - Hotel"
            if quantity is None:
                warnings.append("Missing or invalid hotel nights")
            if unit_warning:
                warnings.append(unit_warning)
        elif "ground" in category_value or "rail" in category_value or "taxi" in category_value:
            quantity = parse_number(first_present(row, ["Distance Km", "Distance", "distance_km", "Miles"]))
            raw_unit = first_present(row, ["Unit", "Distance Unit"], "km")
            unit, unit_warning = normalize_unit(raw_unit)
            category = "Business Travel - Ground"
            if quantity is None:
                warnings.append("Missing or invalid ground transport distance")
            if unit_warning:
                warnings.append(unit_warning)
        else:
            quantity = parse_number(first_present(row, ["Distance Km", "Distance", "distance_km", "Miles"]))
            unit, unit_warning = normalize_unit(first_present(row, ["Unit", "Distance Unit"], "km"))
            category = "Business Travel - Flight"
            if quantity is None and origin and destination:
                quantity = airport_distance_km(origin, destination)
                if quantity is None:
                    warnings.append("Flight distance missing and airport pair is unknown")
                else:
                    warnings.append("Flight distance estimated from airport pair")
            elif quantity is None:
                warnings.append("Missing flight distance and airport pair")
            if unit_warning:
                warnings.append(unit_warning)

        return {
            "source_type": self.source_type,
            "source_reference": str(first_present(row, ["Trip ID", "Expense ID", "Report ID"], "")),
            "scope": "Scope 3",
            "category": category,
            "quantity": quantity,
            "normalized_unit": unit,
            "start_date": start_date,
            "end_date": start_date,
            "raw_data": row,
            "metadata": {
                "origin_airport": str(origin).upper() if origin else "",
                "destination_airport": str(destination).upper() if destination else "",
                "normalization_warnings": warnings,
            },
        }

