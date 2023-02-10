import math


def is_prime(n: int) -> bool:
    """Check if a given int is prime.

    Credits: https://geekflare.com/prime-number-in-python/
    """
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if (n % i) == 0:
            return False
    return True
