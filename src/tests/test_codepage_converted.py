from thermalprinter.constants import CodePageConverted


def test_repr() -> None:
    assert repr(CodePageConverted.CP755) == "CP755       fallback: utf-8"
