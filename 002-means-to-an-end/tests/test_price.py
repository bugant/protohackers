from proto_means_to_an_end import price


def test_avg():
    prices = [
        price.Price(price=101, timestamp=12345),
        price.Price(price=102, timestamp=12346),
        price.Price(price=100, timestamp=12347),
        price.Price(price=5, timestamp=40960),
    ]
    assert 101 == price.avg(prices, 12288, 16384)
