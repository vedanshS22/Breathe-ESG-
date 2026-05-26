from services.normalizers.common import first_present, normalize_unit, parse_number, parse_operational_date


class UtilityNormalizer:
    source_type = "utility"

    def normalize(self, row):
        warnings = []

        quantity = parse_number(first_present(row, ["kWh", "Usage kWh", "Consumption", "Energy Usage"]))
        if quantity is None:
            warnings.append("Missing or invalid electricity usage")

        unit, unit_warning = normalize_unit(first_present(row, ["Unit", "UOM", "Usage Unit"], "kWh"))
        if unit_warning:
            warnings.append(unit_warning)

        start_date, start_warning = parse_operational_date(
            first_present(row, ["Billing Start", "Start Date", "Period Start"])
        )
        end_date, end_warning = parse_operational_date(
            first_present(row, ["Billing End", "End Date", "Period End"])
        )
        if start_warning:
            warnings.append(start_warning)
        if end_warning:
            warnings.append(end_warning)

        meter_id = first_present(row, ["Meter ID", "Meter_ID", "meterNumber", "Meter"], "")
        tariff = first_present(row, ["Tariff", "Rate Plan", "Rate Class"], "")
        account = first_present(row, ["Account Number", "Utility Account", "Account"], "")

        return {
            "source_type": self.source_type,
            "source_reference": str(meter_id or account or ""),
            "scope": "Scope 2",
            "category": "Electricity",
            "quantity": quantity,
            "normalized_unit": unit,
            "start_date": start_date,
            "end_date": end_date,
            "raw_data": row,
            "metadata": {
                "meter_id": meter_id,
                "tariff": tariff,
                "account_number": account,
                "normalization_warnings": warnings,
            },
        }

