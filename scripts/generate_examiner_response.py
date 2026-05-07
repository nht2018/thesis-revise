#!/usr/bin/env python3
"""Generate Chinese examiner-response and advisor-opinion draft materials."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def read_comments(path: str | None) -> str:
    if not path or path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def split_comments(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return ["待填写专家意见。"]

    pattern = re.compile(
        r"(?m)^\s*(?:[-*]\s+|\d+[.)、]\s*|[（(]\d+[）)]\s*|专家[一二三四五六七八九十0-9]+[:：]\s*)"
    )
    starts = [m.start() for m in pattern.finditer(text)]
    if not starts:
        return [" ".join(block.split()) for block in re.split(r"\n\s*\n", text) if block.strip()]

    starts.append(len(text))
    items: list[str] = []
    for i in range(len(starts) - 1):
        block = text[starts[i] : starts[i + 1]].strip()
        block = pattern.sub("", block, count=1).strip()
        if block:
            items.append(" ".join(block.split()))
    return items or ["待填写专家意见。"]


def advisor_text(stance: str) -> str:
    if stance == "conditional":
        return """# 导师意见（草稿，供导师确认）

本人已审阅答辩人针对专家评阅意见所作的修改（或不修改）说明及论文修改稿。答辩人已对专家意见进行了认真核对，并对论文中的主要问题作出了相应修改；对于暂未修改或部分修改的内容，答辩人已说明原因。本人原则同意其对专家意见作出的修改或不修改说明。

答辩人仍需在答辩前进一步核对论文格式、参考文献和文字细节。完成上述完善后，本人同意其参加学位论文答辩。

导师签名：

日期：
"""
    if stance == "not-agree":
        return """# 导师意见（草稿，供导师确认）

本人已审阅答辩人针对专家评阅意见所作的修改（或不修改）说明及论文修改稿。目前部分专家意见尚未得到充分回应，相关修改说明仍需进一步补充和完善。本人暂不同意答辩人当前版本的修改或不修改说明，暂不同意其以该版本参加学位论文答辩。

导师签名：

日期：
"""
    return """# 导师意见（草稿，供导师确认）

本人已审阅答辩人针对专家评阅意见所作的修改（或不修改）说明及论文修改稿。答辩人能够认真对待专家提出的意见，对论文中涉及的文字表述、结构安排、术语记号、参考文献和相关说明等问题进行了逐条核对和相应修改；对于个别未作修改或仅作部分修改的意见，答辩人已结合论文研究内容和实际情况作出说明，理由基本充分。

本人认为，答辩人对专家意见的修改（或不修改）说明较为完整，相关修改能够回应专家意见，论文修改稿已达到申请答辩的要求。本人同意答辩人作出的修改或不修改说明，同意其参加学位论文答辩。

导师签名：

日期：
"""


def build_document(comments: list[str], stance: str, title: str | None, student: str | None) -> str:
    lines: list[str] = []
    lines.append("# 针对专家意见的修改（或不修改）说明")
    lines.append("")
    if title:
        lines.append(f"论文题目：{title}")
    if student:
        lines.append(f"答辩人：{student}")
    if title or student:
        lines.append("")
    lines.append("本人已认真阅读专家对学位论文提出的评阅意见，并在导师指导下对论文进行了逐条核对和修改。现将针对专家意见的修改（或不修改）情况说明如下。")
    lines.append("")
    lines.append("| 序号 | 专家意见 | 修改（或不修改）说明 | 修改位置 |")
    lines.append("| --- | --- | --- | --- |")
    for idx, comment in enumerate(comments, 1):
        safe_comment = comment.replace("|", "\\|")
        lines.append(f"| {idx} | {safe_comment} | 待根据论文实际修改情况填写。 | 待填写。 |")
    lines.append("")
    lines.append("以上说明均基于论文当前修改稿。本人确认已对专家意见进行了认真核对，并已根据论文实际情况作出相应修改或说明。")
    lines.append("")
    lines.append("答辩人签名：")
    lines.append("")
    lines.append("日期：")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(advisor_text(stance).rstrip())
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Chinese examiner-response draft materials.")
    parser.add_argument("comments", nargs="?", help="Plain text file with examiner comments, or stdin if omitted")
    parser.add_argument("--out", help="Output Markdown path; defaults to stdout")
    parser.add_argument("--title", help="Optional thesis title")
    parser.add_argument("--student", help="Optional student name")
    parser.add_argument(
        "--advisor-stance",
        choices=["agree", "conditional", "not-agree"],
        default="agree",
        help="Advisor-opinion draft stance",
    )
    args = parser.parse_args()

    comments = split_comments(read_comments(args.comments))
    doc = build_document(comments, args.advisor_stance, args.title, args.student)
    if args.out:
        Path(args.out).write_text(doc, encoding="utf-8")
    else:
        print(doc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
