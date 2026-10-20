"""校验 notebook：JSON 是否合法、每个代码单元的 Python 语法是否正确。"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from IPython.core.inputtransformer2 import TransformerManager

# IPython 是可选依赖：装了就精确转换魔法命令，没装就退化成简单处理。
# 这里显式标成「可能是 None」，mypy 才知道下面那句 `is None` 是在做空值检查。
_TRANSFORMER: TransformerManager | None
try:
    from IPython.core.inputtransformer2 import TransformerManager

    _TRANSFORMER = TransformerManager()
except Exception:  # noqa: BLE001
    _TRANSFORMER = None


def to_python(source: str) -> str:
    """把 IPython 魔法命令（%timeit、%%time 等）转换成合法 Python。

    直接用 compile() 检查 notebook 会把魔法命令误报成语法错误。
    """
    if _TRANSFORMER is None:
        return "\n".join(
            "# magic" if line.lstrip().startswith(("%", "!")) else line
            for line in source.splitlines()
        )
    return _TRANSFORMER.transform_cell(source)


def check(path: Path) -> bool:
    try:
        nb = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[JSON 错误] {path.name}: {exc}")
        return False

    problems = 0
    for index, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue
        source = "".join(cell["source"])
        try:
            compile(to_python(source), f"{path.name}:cell{index}", "exec")
        except SyntaxError as exc:
            problems += 1
            print(
                f"[语法错误] {path.name} 第 {index} 格，第 {exc.lineno} 行: {exc.msg}"
            )
            line = (exc.text or "").rstrip()
            print(f"          -> {line[:120]}")

    status = "通过" if problems == 0 else f"{problems} 个语法问题"
    print(
        f"{path.name}: JSON 合法，代码单元 {sum(1 for c in nb['cells'] if c['cell_type'] == 'code')} 个，{status}"
    )
    return problems == 0


def main() -> int:
    targets: list[Path] = []
    for arg in sys.argv[1:]:
        path = Path(arg)
        targets.extend(path.rglob("*.ipynb") if path.is_dir() else [path])
    if not targets:
        print("用法: python check_notebooks.py <目录或文件> [...]")
        return 2
    return 0 if all(check(p) for p in targets) else 1


if __name__ == "__main__":
    sys.exit(main())
