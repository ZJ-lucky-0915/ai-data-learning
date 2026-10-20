"""download_data.py 的测试。"""

import pytest

from scripts.download_data import human


def test_1024_字节是_1KB():
    assert human(1024) == "1KB"


def test_0_字节是_0B():
    assert human(0) == "0B"


def test_一兆字节是_1MB():
    assert human(1024**2) == "1MB"


def test_传_None_会报_TypeError():
    """human() 约定接收数字。传 None 说明调用方写错了，让它当场报错。"""
    with pytest.raises(TypeError):
        human(None)
