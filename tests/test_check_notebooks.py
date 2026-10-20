"""check_notebooks.py 的测试。"""

import pytest

from scripts.check_notebooks import check


def test_合法_notebook_返回True(tmp_path):
    nb = tmp_path / "good.ipynb"
    nb.write_text('{"cells": [], "nbformat": 4, "nbformat_minor": 5}', encoding="utf-8")
    assert check(nb) is True


def test_坏掉的_json_返回False(tmp_path):
    nb = tmp_path / "broken.ipynb"
    nb.write_text('{ 这不是 json', encoding="utf-8")
    assert check(nb) is False


def test_空文件(tmp_path):
    nb = tmp_path / "empty.ipynb"
    nb.write_text('', encoding="utf-8")
    assert check(nb) is False


def test_文件不存在会抛错(tmp_path):
    nb = tmp_path / "不存在.ipynb"
    with pytest.raises(FileNotFoundError):
        check(nb)