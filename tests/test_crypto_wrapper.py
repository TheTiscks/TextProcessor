from app.crypto_wrapper import generate_key, using_c


def test_generate_key_length_and_randomness():
    k1 = generate_key(32)
    k2 = generate_key(32)
    assert isinstance(k1, str)
    assert isinstance(k2, str)
    assert len(k1) == 32
    assert len(k2) == 32
    # строки могут совпасть, но это маловероятно
    assert k1 != k2


def test_using_c_flag_type():
    # using_c() -> bool?
    assert isinstance(using_c(), bool)
