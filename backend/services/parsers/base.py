import csv
import io
import json
from dataclasses import dataclass
from pathlib import Path

from services.exceptions import ParserError


ENCODINGS = ("utf-8-sig", "utf-8", "cp1252", "latin1")


@dataclass
class ParsedRow:
    row_number: int
    data: dict


def normalize_header(value):
    return str(value or "").strip().lower().replace("_", " ").replace("-", " ")


def read_upload_bytes(file_obj):
    if hasattr(file_obj, "open"):
        file_obj.open("rb")
    try:
        content = file_obj.read()
    finally:
        if hasattr(file_obj, "seek"):
            file_obj.seek(0)
    return content


def decode_bytes(content):
    for encoding in ENCODINGS:
        try:
            return content.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise ParserError("Could not decode file using utf-8, cp1252, or latin1.")


class BaseCsvParser:
    required_alias_groups = {}

    def parse(self, file_obj):
        content = read_upload_bytes(file_obj)
        if not content or not content.strip():
            raise ParserError("Uploaded file is empty.")

        text, _encoding = decode_bytes(content)
        sample = text[:4096]

        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        except csv.Error:
            dialect = csv.excel

        reader = csv.reader(io.StringIO(text), dialect)
        try:
            headers = next(reader)
        except StopIteration as exc:
            raise ParserError("Uploaded file has no header row.") from exc

        clean_headers = [header.strip() for header in headers]
        normalized_headers = [normalize_header(header) for header in clean_headers]
        if len(normalized_headers) != len(set(normalized_headers)):
            raise ParserError("Duplicate headers make the source mapping ambiguous.")

        self._validate_required_headers(normalized_headers)

        rows = []
        for row_number, row in enumerate(reader, start=2):
            if not row or all(str(cell).strip() == "" for cell in row):
                continue
            if len(row) != len(clean_headers):
                rows.append(
                    ParsedRow(
                        row_number=row_number,
                        data={
                            "__parse_error__": (
                                f"Expected {len(clean_headers)} columns, found {len(row)}."
                            ),
                            "__raw_row__": row,
                        },
                    )
                )
                continue

            rows.append(
                ParsedRow(
                    row_number=row_number,
                    data={header: value.strip() for header, value in zip(clean_headers, row)},
                )
            )

        return rows

    def _validate_required_headers(self, normalized_headers):
        for label, aliases in self.required_alias_groups.items():
            normalized_aliases = {normalize_header(alias) for alias in aliases}
            if not normalized_aliases.intersection(normalized_headers):
                raise ParserError(f"Missing required {label} column.")


class JsonListParser:
    required_alias_groups = {}

    def parse(self, file_obj):
        content = read_upload_bytes(file_obj)
        if not content or not content.strip():
            raise ParserError("Uploaded file is empty.")
        text, _encoding = decode_bytes(content)
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ParserError("JSON file could not be parsed.") from exc

        if isinstance(payload, dict):
            payload = payload.get("results") or payload.get("records") or payload.get("data")
        if not isinstance(payload, list):
            raise ParserError("JSON travel exports must contain a list of records.")

        rows = []
        for index, item in enumerate(payload, start=1):
            if not isinstance(item, dict):
                rows.append(
                    ParsedRow(
                        row_number=index,
                        data={"__parse_error__": "JSON row is not an object.", "__raw_row__": item},
                    )
                )
                continue
            rows.append(ParsedRow(row_number=index, data=item))
        return rows


def get_extension(filename):
    return Path(filename or "").suffix.lower()

