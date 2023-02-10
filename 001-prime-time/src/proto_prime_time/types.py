import attr

VALID_METHOD = "isPrime"


def _valid_method(instance, attribute, value) -> None:
    if not (value == VALID_METHOD):
        raise ValueError(f"invalid method {value}")


def _int_or_float(instance, attribute, value) -> None:
    # bool values are instance of int, so filter out them
    if isinstance(value, bool) or not any(isinstance(value, t) for t in [int, float]):
        raise ValueError(f"unsupported type for number {type(value)}")


@attr.define
class Request:
    method: str = attr.field(validator=_valid_method)
    number: int | float = attr.field(validator=_int_or_float)


@attr.define
class Response:
    method: str = attr.field(validator=_valid_method)
    prime: bool
