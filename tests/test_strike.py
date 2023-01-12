def test_default_value(printer):
    assert printer._strike is False


def test_changing_no_value(printer):
    printer.strike()
    assert printer._strike is False


def test_changing_state_on(printer):
    printer.strike(True)
    assert printer._strike is True


def test_changing_state_off(printer):
    printer.strike(False)
    assert printer._strike is False


def test_reset_value(printer):
    printer.reset()
    assert printer._strike is False
