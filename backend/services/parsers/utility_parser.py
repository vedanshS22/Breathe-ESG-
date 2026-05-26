from services.parsers.base import BaseCsvParser


class UtilityPortalCsvParser(BaseCsvParser):
    required_alias_groups = {
        "electricity usage": ["kWh", "Usage kWh", "Consumption", "Energy Usage"],
        "billing start": ["Billing Start", "Start Date", "Period Start"],
        "billing end": ["Billing End", "End Date", "Period End"],
    }

