import wasmtime.loader
from alg import fibonacci, prime
from util import timethis
# pyright: reportMissingImports=false
import wasi_alg


@timethis
def timed_fibonacci(n):
    return fibonacci(n)


@timethis
def timed_rust_fibonacci(n):
    return wasi_alg.fibonacci(n)


@timethis
def timed_prime(n):
    return prime(n)


@timethis
def timed_rust_prime(n):
    return wasi_alg.prime(n)


if __name__ == "__main__":
    print("\nTime fibonacci python:")
    assert timed_fibonacci(30) == 832040
    print("\nTime fibonacci wasm:")
    assert timed_rust_fibonacci(30) == 832040

    print("\nTime prime python:")
    assert timed_prime(10000) == 104743
    print("\nTime prime wasm:")
    assert timed_rust_prime(10000) == 104743
