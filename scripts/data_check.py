"""数据体检脚本：拿到一份新数据，先跑它。

用法:
    python scripts/data_check.py data/raw/titanic.csv
    python scripts/data_check.py data/raw/tmdb_5000_movies.csv --rows 5

设计思路：孤立的数字没有意义，**每个数字都要有对照物**。
本脚本把"该跟什么比"自动化，把可疑信号标出来，剩下的判断留给你。
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def section(title: str) -> None:
    print()
    print(f"{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def check_shape(df: pd.DataFrame) -> None:
    section("1. 形状与类型")
    print(f"  行数: {len(df):,}    列数: {df.shape[1]}")
    numeric = df.select_dtypes("number").columns.tolist()
    others = [c for c in df.columns if c not in numeric]
    print(f"  数值列 ({len(numeric)}): {numeric}")
    print(f"  非数值列 ({len(others)}): {others}")
    print()
    print("  每一列的类型：")
    for column, dtype in df.dtypes.items():
        print(f"    {column:22s} {dtype}")


def check_missing(df: pd.DataFrame) -> None:
    section("2. 缺失情况")
    missing = df.isna().sum()
    if missing.sum() == 0:
        print("  没有缺失值。")
        return

    ratio = (missing / len(df) * 100).round(1)
    table = pd.DataFrame({"缺失数量": missing, "缺失比例%": ratio})
    table = table[table["缺失数量"] > 0].sort_values("缺失比例%", ascending=False)
    print(table.to_string())
    print()
    print("  怎么读：")
    for column, row in table.iterrows():
        share = row["缺失比例%"]
        if share >= 50:
            hint = "缺失过半，硬填等于编造数据 → 考虑「标记」成一列新特征"
        elif share <= 5:
            hint = "缺得极少 → 通常直接丢掉这几行最省事"
        else:
            hint = "缺得不多不少 → 填中位数/众数，或者标记"
        print(f"    {column:22s} {share:>5}%   {hint}")


def check_numeric(df: pd.DataFrame) -> None:
    section("3. 数值列对照表")
    numeric = df.select_dtypes("number")
    if numeric.empty:
        print("  没有数值列。")
        return

    rows = []
    for column in numeric.columns:
        series = df[column].dropna()
        if series.empty:
            continue
        mean, median = series.mean(), series.median()
        ratio = mean / median if median else float("nan")
        rows.append(
            {
                "列": column,
                "最小": series.min(),
                "25%": series.quantile(0.25),
                "中位数": median,
                "均值": mean,
                "75%": series.quantile(0.75),
                "最大": series.max(),
                "均值/中位数": ratio,
                "标准差": series.std(),
            }
        )

    table = pd.DataFrame(rows).set_index("列")
    print(table.round(2).to_string())
    print()
    print("  自动标注的可疑信号：")
    flagged = False
    for column, row in table.iterrows():
        notes = []
        ratio = row["均值/中位数"]
        if pd.notna(ratio) and ratio > 1.5:
            notes.append(f"均值是 Median 的 {ratio:.1f} 倍 → 右偏，有高价极端值拉着均值跑")
        elif pd.notna(ratio) and ratio < 0.67:
            notes.append(f"均值只有中位数的 {ratio:.2f} 倍 → 左偏")
        if row["最小"] == 0 and row["中位数"] > 0:
            zeros = int((df[column] == 0).sum())
            notes.append(f"最小值为 0（{zeros} 个）→ 这类值是真的吗？还是缺失被填成 0？")
        is_binary = df[column].nunique(dropna=True) <= 2
        if not is_binary and row["标准差"] > abs(row["均值"]) and row["均值"] != 0:
            notes.append(f"标准差({row['标准差']:.1f}) 比均值({row['均值']:.1f}) 还大 → 波动极大")
        if row["75%"] > 0 and row["最大"] > row["75%"] * 5:
            notes.append(f"最大值({row['最大']:.1f}) 是中位数 75% 分位({row['75%']:.1f}) 的 5 倍以上 → 长尾")
        if notes:
            flagged = True
            print(f"    [{column}]")
            for note in notes:
                print(f"      - {note}")
    if not flagged:
        print("    没有明显异常。")


def check_categorical(df: pd.DataFrame, max_unique: int = 12) -> None:
    section("4. 类别列取值分布")
    for column in df.columns:
        unique = df[column].nunique(dropna=True)
        if unique > max_unique:
            print(f"  {column:22s} 取值 {unique:,} 种（太多，跳过）")
            continue
        counts = df[column].value_counts(dropna=False)
        detail = ", ".join(f"{k}={v}" for k, v in counts.items())
        print(f"  {column:22s} {unique} 种: {detail}")


def check_suspicious(df: pd.DataFrame) -> None:
    section("5. 可疑值扫描")
    issues = 0

    duplicated = int(df.duplicated().sum())
    print(f"  完全重复的行: {duplicated}" + ("  ← 要查清楚，可能是重复录入" if duplicated else ""))
    issues += bool(duplicated)

    for column in df.columns:
        unique = df[column].nunique(dropna=True)
        if unique == len(df):
            kind = "文本" if pd.api.types.is_string_dtype(df[column]) else "数值"
            print(
                f"  {column}: 每一行的值都不同（{kind}列）→ "
                "如果是编号，就是 ID、对分析没用；如果是名称/票号这类文本，"
                "先看看能不能拆出信息（比如称谓、前缀、单号规律）"
            )
            issues += 1
        elif unique == 1:
            print(f"  {column}: 只有一个取值 → 没有任何信息量")
            issues += 1

    non_numeric = df.select_dtypes(exclude="number")
    for column in non_numeric.columns:
        blanks = int((non_numeric[column].astype("string").str.strip() == "").sum())
        if blanks:
            print(f"  {column}: 有 {blanks} 个空字符串（不是 NaN，是空文本）")
            issues += 1

    repeats = df.columns[df.columns.duplicated()].tolist()
    if repeats:
        print(f"  重复的列名: {repeats}")
        issues += 1

    if not issues:
        print("  没有发现。")


def main() -> None:
    parser = argparse.ArgumentParser(description="数据体检")
    parser.add_argument("path", nargs="?", help="CSV 或 Parquet 文件的路径")
    parser.add_argument("--rows", type=int, default=3, help="打印前几行样本")
    args = parser.parse_args()

    if not args.path:
        print("你没有给数据文件路径。正确用法：")
        print("    python scripts/data_check.py <数据文件路径>")
        print()
        raw = Path("data/raw")
        if raw.is_dir():
            files = sorted(p for p in raw.iterdir() if p.suffix in {".csv", ".parquet"})
            if files:
                print("data/raw/ 里现成的数据，直接抄一行去用：")
                for item in files:
                    print(f"    python scripts/data_check.py {item.as_posix()}")
            else:
                print("data/raw/ 里还没有数据文件，先跑 python scripts/download_data.py")
        else:
            print("当前目录下找不到 data/raw/ —— 你多半不在项目根目录。先执行：")
            print('    cd "D:\\Codex Project\\AI-Data"')
        return

    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"文件不存在: {path.resolve()}")

    df = pd.read_parquet(path) if path.suffix == ".parquet" else pd.read_csv(path)

    print(f"文件: {path}")
    print(f"体检开始（这是一份自动化清单，结论要你自己下）")

    check_shape(df)
    check_missing(df)
    check_numeric(df)
    check_categorical(df)
    check_suspicious(df)

    section("6. 前几行样本")
    print(df.head(args.rows).to_string())

    section("体检完毕")
    print("  下一步：把上面标出来的每一条，问自己「这正常吗？可能意味着什么？」")
    print("  有 3 条以上可疑点，就可以开始写你的分析了。")


if __name__ == "__main__":
    main()
