import pytest

from proto_prime_time import api, types


@pytest.mark.parametrize('req,resp', (
    ({}, None),
    ({"foo": "bar"}, None),
    ({"method": "isPrime", "number": 2}, types.Response(method="isPrime", prime=True)),
    ({"method": "isPrime", "number": 4}, types.Response(method="isPrime", prime=False)),
    ({"method": "isPrime", "number": 3, "foo": "bar"}, types.Response(method="isPrime", prime=True)),
))
def test_api(req, resp):
    assert resp == api.process_request(req)
