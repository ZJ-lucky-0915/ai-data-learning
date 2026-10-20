"""pytest 全局配置。

Windows 上 C:\\Users\\<用户>\\AppData\\Local\\Temp\\pytest-of-* 这个目录权限损坏时，
pytest 一启动就会 PermissionError，所有测试直接报错（还没跑到测试代码）。
这里把临时目录固定到项目里的 .pytest_tmp，不再碰系统 Temp。
"""

from __future__ import annotations

from pathlib import Path


def pytest_configure(config) -> None:
    if getattr(config.option, "basetemp", None):
        return
    config.option.basetemp = str(Path(__file__).resolve().parent / ".pytest_tmp")
