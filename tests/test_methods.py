# coding: utf-8

import inspect
import types


from thermalprinter.constants import BarCodePosition, CharSet, Chinese, \
    CodePage
from thermalprinter import ThermalPrinter

import pytest


@pytest.fixture(scope="module")
def methods():
    return list(sorted([x for x, y in ThermalPrinter.__dict__.items()
                        if isinstance(y, types.FunctionType)]))


@pytest.mark.parametrize(
    "method, arguments",
    [
        ("__enter__", {}),
        ("__init__", {"args": ["self", "port", "baudrate"],
                      "varkw": "kwargs",
                      "defaults": ("/dev/ttyAMA0", 19200)}),
        ("__repr__", {}),
        ("_on_exit", {}),
        ("barcode", {"args": ["self", "data", "barcode_type"]}),
        ("barcode_height", {"args": ["self", "height"], "defaults": (162,)}),
        ("barcode_left_margin", {"args": ["self", "margin"], "defaults": (0,)}),
        ("barcode_position", {"args": ["self", "position"], "defaults": (BarCodePosition.HIDDEN,)}),
        ("barcode_width", {"args": ["self", "width"], "defaults": (3,)}),
        ("bold", {"args": ["self", "state"], "defaults": (False,)}),
        ("charset", {"args": ["self", "charset"], "defaults": (CharSet.USA,)}),
        ("char_spacing", {"args": ["self", "spacing"], "defaults": (0,)}),
        ("chinese", {"args": ["self", "state"], "defaults": (False,)}),
        ("chinese_format", {"args": ["self", "fmt"], "defaults": (Chinese.GBK,)}),
        ("codepage", {"args": ["self", "codepage"], "defaults": (CodePage.CP437,)}),
        ("double_height", {"args": ["self", "state"], "defaults": (False,)}),
        ("double_width", {"args": ["self", "state"], "defaults": (False,)}),
        ("feed", {"args": ["self", "number"], "defaults": (1,)}),
        ("flush", {"args": ["self", "clear"], "defaults": (False,)}),
        ("image", {"args": ["self", "image"]}),
        ("inverse", {"args": ["self", "state"], "defaults": (False,)}),
        ("justify", {"args": ["self", "value"], "defaults": ("L",)}),
        ("left_margin", {"args": ["self", "margin"], "defaults": (0,)}),
        ("line_spacing", {"args": ["self", "spacing"], "defaults": (30,)}),
        ("offline", {}),
        ("online", {}),
        ("out", {"args": ["self", "data", "line_feed"],
                 "varkw": "kwargs", "defaults": (True,)}),
        ("rotate", {"args": ["self", "state"], "defaults": (False,)}),
        ("send_command", {"varargs": "args"}),
        ("size", {"args": ["self", "value"], "defaults": ("S",)}),
        ("sleep", {"args": ["self", "seconds"], "defaults": (1,)}),
        ("status", {"args": ["self", "raise_on_error"], "defaults": (True,)}),
        ("strike", {"args": ["self", "state"], "defaults": (False,)}),
        ("reset", {}),
        ("test", {}),
        ("to_bytes", {"args": ["self", "data"]}),
        ("underline", {"args": ["self", "weight"], "defaults": (0,)}),
        ("upside_down", {"args": ["self", "state"], "defaults": (False,)}),
        ("wake", {}),
    ]
)
def test_signature(methods, method, arguments):
    methods.remove(method)

    args = {"args": ["self"], "varargs": None, "varkw": None,
            "defaults": None, "kwonlyargs": [],
            "kwonlydefaults": None, "annotations": {},
            **arguments}
    sig = inspect.FullArgSpec(**args)
    spec = inspect.getfullargspec(getattr(ThermalPrinter, method))
    assert spec == sig


def test__orphans(methods):
    assert not methods
