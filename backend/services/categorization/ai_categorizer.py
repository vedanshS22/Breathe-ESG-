import csv
import io
from services.exceptions import IngestionError, ParserError
from services.parsers.base import decode_bytes, read_upload_bytes


SOURCE_SIGNALS = {
    "sap": {
        "werk",
        "plant",
        "buchungsdatum",
        "budat",
        "material document",
        "mblnr",
        "kraftstoff",
        "menge",
        "einheit",
    },
    "utility": {
        "meter id",
        "meter",
        "utility account",
        "billing start",
        "billing end",
        "period start",
        "period end",
        "usage kwh",
        "kwh",
        "tariff",
    },
    "travel": {
        "trip id",
        "expense id",
        "report id",
        "from airport",
        "to airport",
        "origin airport",
        "destination airport",
        "trip date",
        "travel type",
    },
}


SCOPE_CATEGORY_RULES = {
    "sap": ("Scope 1", "Fuel"),
    "utility": ("Scope 2", "Electricity"),
    "travel": ("Scope 3", "Business Travel"),
}


class AICategorizer:
    """
    Local classifier-style categorizer.

    The project intentionally avoids a network LLM dependency in the ingestion path.
    This service behaves like an AI categorization layer: it scores file structure and
    field names, returns a confidence score, and stores its decision metadata.
    """

    def infer_source_type(self, uploaded_file):
        content = read_upload_bytes(uploaded_file)
        filename = getattr(uploaded_file, "name", "")
        if filename.lower().endswith(".json"):
            return {
                "source_type": "travel",
                "confidence": 0.9,
                "signals": ["JSON travel exports are the only JSON source supported"],
            }

        try:
            text, _encoding = decode_bytes(content)
        except ParserError as exc:
            raise IngestionError(str(exc)) from exc
        headers = self._read_csv_headers(text)
        if not headers:
            raise IngestionError("Auto categorization could not find a header row.")

        normalized_headers = {self._normalize_header(header) for header in headers}
        scores = {}
        matched_signals = {}
        for source_type, signals in SOURCE_SIGNALS.items():
            matches = sorted(signals.intersection(normalized_headers))
            scores[source_type] = len(matches)
            matched_signals[source_type] = matches

        source_type, score = max(scores.items(), key=lambda item: item[1])
        if score == 0:
            raise IngestionError("Auto categorization could not identify the source type from file headers.")

        total_known_headers = sum(scores.values()) or 1
        confidence = round(min(0.98, max(0.55, score / total_known_headers)), 2)
        return {
            "source_type": source_type,
            "confidence": confidence,
            "signals": matched_signals[source_type],
        }

    def categorize_record(self, normalized_record, source_decision, mode):
        source_type = normalized_record.get("source_type")
        expected_scope, default_category = SCOPE_CATEGORY_RULES.get(source_type, ("", ""))
        metadata = dict(normalized_record.get("metadata") or {})
        metadata["categorization"] = {
            "mode": mode,
            "method": "rules_plus_header_classifier",
            "source_type_confidence": source_decision.get("confidence") if source_decision else None,
            "signals": source_decision.get("signals", []) if source_decision else [],
            "scope_decision": normalized_record.get("scope") or expected_scope,
            "category_decision": normalized_record.get("category") or default_category,
        }
        return {**normalized_record, "metadata": metadata}

    def _read_csv_headers(self, text):
        sample = text[:4096]
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        except csv.Error:
            dialect = csv.excel
        reader = csv.reader(io.StringIO(text), dialect)
        try:
            return next(reader)
        except StopIteration:
            return []

    def _normalize_header(self, value):
        return str(value or "").strip().lower().replace("_", " ").replace("-", " ")
