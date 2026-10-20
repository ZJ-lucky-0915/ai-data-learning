"""把学习用的公开数据集下载到 data/raw/。

用法:
    python scripts/download_data.py            # 下载全部可自动获取的
    python scripts/download_data.py titanic    # 只下 titanic
    python scripts/download_data.py --list     # 看有哪些数据集

说明:
- Titanic 走 GitHub 上的公开镜像，不需要 Kaggle 账号。
- TMDB 的官方来源在 Kaggle，需要登录。脚本会先试公开镜像，全部失败时打印手动步骤。
- IMDB 影评数据集在阶段 4 用 HuggingFace 的 datasets 库直接拉取，这里不处理。
"""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# 每个数据集给多个候选来源，逐个尝试，第一个成功的就用
SOURCES: dict[str, list[tuple[str, str]]] = {
    "titanic": [
        (
            "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv",
            "titanic.csv",
        ),
    ],
    "tmdb": [
        # HuggingFace 上的公开镜像（GitHub 上流传的那些 tmdb_5000_movies.csv 链接基本都失效了）
        (
            "https://huggingface.co/datasets/alejandrowallace/tmdb-5000/resolve/main/tmdb_5000_movies.csv",
            "tmdb_5000_movies.csv",
        ),
        (
            "https://huggingface.co/datasets/AiresPucrs/tmdb-5000-movies/resolve/main/tmdb_5000_movies.csv",
            "tmdb_5000_movies.csv",
        ),
    ],
}

MANUAL_HINT = """
如果上面的镜像都失效了，走 Kaggle 官方来源：
  1. 注册并登录 https://www.kaggle.com
  2. 头像 -> Settings -> API -> Create New Token，得到 kaggle.json
  3. 把 kaggle.json 放到 C:\\Users\\<你的用户名>\\.kaggle\\kaggle.json
  4. 执行: kaggle datasets download -d tmdb/tmdb-movie-metadata -p data\\raw --unzip
"""


def human(size: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.0f}{unit}"
        size /= 1024
    return f"{size:.0f}TB"


def fetch(url: str, dest: Path, timeout: int = 30) -> None:
    """下载 url 到 dest。先写临时文件再改名，避免留下半截文件。"""
    request = urllib.request.Request(
        url, headers={"User-Agent": "ai-data-learning/1.0"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read()
    if not data:
        raise ValueError("下载到 0 字节，来源可能已失效")
    tmp = dest.with_suffix(dest.suffix + ".part")
    tmp.write_bytes(data)
    tmp.replace(dest)


def download(name: str) -> bool:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for url, filename in SOURCES[name]:
        dest = RAW_DIR / filename
        if dest.exists() and dest.stat().st_size > 0:
            print(f"  [跳过] {filename} 已存在（{human(dest.stat().st_size)}）")
            return True
        print(f"  尝试 {url}")
        try:
            fetch(url, dest)
        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            OSError,
            ValueError,
        ) as exc:
            print(f"    -> 失败：{type(exc).__name__}: {exc}")
            continue
        print(f"    -> 成功：{dest.name}（{human(dest.stat().st_size)}）")
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="下载学习用的数据集")
    parser.add_argument("datasets", nargs="*", help="要下载的数据集名，留空表示全部")
    parser.add_argument("--list", action="store_true", help="列出可选数据集")
    args = parser.parse_args()

    if args.list:
        for key in SOURCES:
            print(f"  {key}")
        return 0

    unknown = [name for name in args.datasets if name not in SOURCES]
    if unknown:
        print(f"不认识的数据集：{', '.join(unknown)}；可选：{', '.join(SOURCES)}")
        return 2

    targets = args.datasets or list(SOURCES)
    print(f"下载目录：{RAW_DIR}\n")

    failed: list[str] = []
    for name in targets:
        print(f"[{name}]")
        if not download(name):
            failed.append(name)
            if name == "tmdb":
                print(MANUAL_HINT)
        print()

    if failed:
        print(f"未获取到：{', '.join(failed)}（其它数据集不受影响）")
        return 1 if len(failed) == len(targets) else 0

    print("全部就绪。数据在 data/raw/ 下，接下来可以在 notebook 里读了。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
