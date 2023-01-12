def test_default_value(printer):
    assert printer._double_height is False
    assert printer._char_height == 24


def test_changing_no_value(printer):
    printer.double_height()
    assert printer._double_height is False
    assert printer._char_height == 24


def test_changing_state_on(printer):
    printer.double_height(True)
    assert printer._double_height is True
    assert printer._char_height == 48


def test_changing_state_off(printer):
    printer.double_height(False)
    assert printer._double_height is False
    assert printer._char_height == 24


def test_reset_value(printer):
    printer.reset()
    assert printer._double_height is False
    assert printer._char_height == 24
