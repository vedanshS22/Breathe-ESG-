from services.exceptions import ParserError
from services.parsers.base import get_extension
from services.parsers.sap_parser import SapFlatFileParser
from services.parsers.travel_parser import TravelCsvParser, TravelJsonParser
from services.parsers.utility_parser import UtilityPortalCsvParser


def get_parser(source_type, filename):
    extension = get_extension(filename)
    if source_type == "sap" and extension == ".csv":
        return SapFlatFileParser()
    if source_type == "utility" and extension == ".csv":
        return UtilityPortalCsvParser()
    if source_type == "travel" and extension == ".csv":
        return TravelCsvParser()
    if source_type == "travel" and extension == ".json":
        return TravelJsonParser()
    raise ParserError("Unsupported file type for this source.")

