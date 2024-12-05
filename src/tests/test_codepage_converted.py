from thermalprinter.constants import CodePageConverted


def test_repr() -> None:
    assert repr(CodePageConverted.CP755) == "utf-8"


def test_str() -> None:
    assert str(CodePageConverted.CP755) == "CP755"
