#!/usr/bin/env python3
"""text_stats.py - 独立的英文文本词频统计程序。

用法:
    python code/text_stats.py <文本文件路径> [-n N]

功能:
    * 以 UTF-8 读取文本文件;
    * 提取英文单词（大小写不敏感）并统计出现次数;
    * 按出现次数降序输出前 N 个单词，格式为「单词 次数 占比%」。

该程序只依赖 Python 标准库，可单独复制到任意目录运行。
"""

import argparse
import re
import sys
from collections import Counter

# 匹配英文单词: 允许单词内部出现连字符与撇号，如 e-mail、don't。
WORD_PATTERN = re.compile(r"[A-Za-z]+(?:['\-][A-Za-z]+)*")


def load_text(path: str) -> str:
    """以 UTF-8 编码读取文本文件内容。"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def count_words(text: str) -> Counter:
    """统计英文单词出现次数，返回 Counter（键为小写单词）。"""
    return Counter(WORD_PATTERN.findall(text.lower()))


def ranking(counter: Counter, top_n: int):
    """按「次数降序、同次数按字母升序」返回前 top_n 项，保证结果稳定。"""
    return sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:top_n]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="text_stats.py",
        description="统计英文文本词频并输出 Top-N（单词 次数 占比%）",
    )
    parser.add_argument("path", help="输入文本文件路径（UTF-8 编码）")
    parser.add_argument(
        "-n",
        "--top",
        type=int,
        default=10,
        metavar="N",
        help="输出的单词个数，默认 10",
    )
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.top < 0:
        parser.error("top N 不能为负数")

    try:
        text = load_text(args.path)
    except FileNotFoundError:
        print(f"错误: 找不到文件 {args.path}", file=sys.stderr)
        return 2
    except IsADirectoryError:
        print(f"错误: {args.path} 是一个目录，不是文本文件", file=sys.stderr)
        return 2
    except UnicodeDecodeError:
        print(f"错误: {args.path} 不是有效的 UTF-8 文本文件", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"错误: 无法读取 {args.path} ({exc})", file=sys.stderr)
        return 2

    counter = count_words(text)
    total = sum(counter.values())

    print(f"文件: {args.path}")
    if total == 0:
        print("未在文件中找到英文单词。")
        return 0
    print(f"总词数: {total}, 不同单词数: {len(counter)}")
    print(f"出现频率最高的前 {args.top} 个单词")
    print("-" * 40)
    for word, cnt in ranking(counter, args.top):
        print(f"{word:<20} {cnt:>6}  {cnt / total * 100:.2f}%")

    return 0


if __name__ == "__main__":
    sys.exit(main())
