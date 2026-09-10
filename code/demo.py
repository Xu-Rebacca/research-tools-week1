"""demo.py - 简单的英文文本词频统计程序（实验一：Git 基础练习）"""

import re
import sys
from collections import Counter


def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def count_words(text: str) -> Counter:
    # 仅保留字母，统一转为小写
    words = re.findall(r"[a-zA-Z']+", text.lower())
    return Counter(words)


def main() -> None:
    if len(sys.argv) < 2:
        print("用法: python demo.py <文本文件路径> [top N]")
        sys.exit(1)

    path = sys.argv[1]
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    text = load_text(path)
    counter = count_words(text)
    total = sum(counter.values())

    print(f"文件: {path}")
    print(f"总词数: {total}, 不同单词数: {len(counter)}\n")
    print(f"出现频率最高的前 {top_n} 个单词:")
    print("-" * 30)
    for word, cnt in counter.most_common(top_n):
        print(f"{word:<20} {cnt:>6}  {cnt / total * 100:.2f}%")


if __name__ == "__main__":
    main()
