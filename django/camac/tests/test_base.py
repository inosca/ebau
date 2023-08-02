from ..base import Base, base10

_base62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def test_base_generic():
    for base in range(60):
        base_x = Base(_base62[: base + 2])
        for num in range(100):
            assert base_x.decode(base_x.encode(num)) == num


def test_base_examples():
    assert base10.encode(15) == "15"
    assert base10.encode(4242) == "4242"
    assert base10.decode("4242") == 4242
