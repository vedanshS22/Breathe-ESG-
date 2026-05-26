class IngestionError(Exception):
    """Operational ingestion failure that can be shown safely to the analyst."""


class ParserError(IngestionError):
    pass


class NormalizationError(IngestionError):
    pass


class WorkflowConflict(Exception):
    """Invalid workflow transition, usually returned as HTTP 409."""

