# coding: utf-8


def test_default_state(printer):
    assert printer.is_online is True


def test_online(printer):
    printer.online()
    assert printer.is_online is True


def test_offline(printer):
    printer.offline()
    assert printer.is_online is False


def test_online_after_offline(printer):
    printer.online()
    assert printer.is_online is True


def test_reset_value(printer):
    printer.reset()
    assert printer.is_online is True
