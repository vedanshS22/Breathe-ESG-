from services.exceptions import NormalizationError
from services.normalizers.sap_normalizer import SapNormalizer
from services.normalizers.travel_normalizer import TravelNormalizer
from services.normalizers.utility_normalizer import UtilityNormalizer


NORMALIZERS = {
    "sap": SapNormalizer,
    "utility": UtilityNormalizer,
    "travel": TravelNormalizer,
}


def get_normalizer(source_type):
    try:
        return NORMALIZERS[source_type]()
    except KeyError as exc:
        raise NormalizationError("Unsupported source type.") from exc

