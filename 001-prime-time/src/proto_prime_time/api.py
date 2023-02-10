import logging

from proto_prime_time import prime, types

MALFORMED_RESPONSE = {}
logger = logging.getLogger(__name__)


def process_request(req: dict) -> types.Response | None:
    """Process an incoming request

    If the request is malformed, returns None
    otherwise a proper response will be built.
    """
    try:
        request = request_from_dict(req)
    except Exception:
        return None

    return types.Response(
        method=types.VALID_METHOD,
        prime=(isinstance(request.number, int) and prime.is_prime(request.number)),
    )


def request_from_dict(req: dict) -> types.Request:
    try:
        return types.Request(method=req["method"], number=req["number"])
    except Exception:
        logger.exception(f"malformed request {req}")
        raise
