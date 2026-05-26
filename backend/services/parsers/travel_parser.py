from services.parsers.base import BaseCsvParser, JsonListParser


class TravelCsvParser(BaseCsvParser):
    required_alias_groups = {
        "travel category": ["Category", "Trip Type", "Travel Type", "Expense Type"],
        "activity date": ["Trip Date", "Booking Date", "Transaction Date", "Start Date"],
    }


class TravelJsonParser(JsonListParser):
    pass

