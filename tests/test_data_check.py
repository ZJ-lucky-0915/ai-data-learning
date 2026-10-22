"""data_check.py的测试"""

import pandas as pd

from scripts.data_check import check_missing, section


def test_section_会打印title和分割线(capsys):
    section("测试标题")

    out = capsys.readouterr().out

    assert "测试标题" in out
    assert "=" * 60 in out


def test_只有缺失行会被打印(capsys):
    df = pd.DataFrame({"a": [1, 2, None], "b": [1, 2, 3]})
    check_missing(df)

    out = capsys.readouterr().out

    assert "33.3" in out
    assert "b" not in out
