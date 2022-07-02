def fibonacci(n):
    if n < 2:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)

def prime(n):
    # type: (int) -> int
    """Calculates the nth prime number."""
    if n == 0:
        return 2

    primes = [3]
    recent = 3
    count = 1

    while count < n:
        recent += 2
        is_prime = True

        for item in primes:
            if recent % item == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(recent)
            count += 1

    return primes[n - 1]