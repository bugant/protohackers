import math
import typing

import attrs


@attrs.define
class Price:
    timestamp: int
    price: int


def avg(prices: typing.Sequence[Price], tmin: int, tmax: int) -> int:
    """Calculate the average price between the given timestamps.

    NOTE: This implementation uses a simple sequence to store prices
          and iterate through the whole database when answering a query.
          This is very inefficent, but here we are focusing on the
          networking part of the story, so I kept this as simple as possible.
    """
    price_sum = 0
    price_count = 0
    for price in prices:
        if tmin <= price.timestamp and tmax >= price.timestamp:
            price_sum += price.price
            price_count += 1

    if not price_count:
        return 0
    return math.floor(price_sum/price_count)
