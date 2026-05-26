from rest_framework.response import Response


def success(data=None, status_code=200, **extra):
    payload = {"success": True}
    if data is not None:
        payload["data"] = data
    payload.update(extra)
    return Response(payload, status=status_code)


def failure(error, status_code=400, validation_errors=None):
    payload = {"success": False, "error": error}
    if validation_errors:
        payload["validation_errors"] = validation_errors
    return Response(payload, status=status_code)

