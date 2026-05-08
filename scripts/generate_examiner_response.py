#!/usr/bin/env python3
"""Generate Chinese examiner-response and advisor-opinion draft materials."""

from __future__ import annotations

import argparse
import json
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


def load_approval(path: str | None) -> dict:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_comment_status(path: str | None) -> dict[int, dict]:
    if not path:
        return {}
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(raw, list):
        result = {}
        for item in raw:
            if isinstance(item, dict) and "comment_index" in item:
                result[int(item["comment_index"])] = item
        return result
    if isinstance(raw, dict):
        return {int(key): value for key, value in raw.items()}
    return {}


def approval_summary(approval: dict, item: dict | None = None) -> tuple[str, str, str]:
    if item:
        status = item.get("status", "").strip()
        explanation = item.get("explanation", "").strip()
        location = item.get("location", "").strip()
        approved = item.get("approved_ids") or item.get("approved_items") or []
        ignored = item.get("ignored_ids") or item.get("ignored_items") or []
        unapproved = item.get("unapproved_ids") or item.get("unapproved_items") or []
        cancelled = item.get("cancelled", False)
        if status and explanation:
            return (status, explanation, location or "待填写。")
        if cancelled:
            return ("审批取消", "相关修改审批流程已取消，故本次暂未形成最终修改。", location or "不适用。")
        if approved and (ignored or unapproved):
            return ("部分修改", "部分修改建议已获批准并应填写已完成的修改内容；未获批准或已忽略的部分应说明暂未修改原因。", location or "待填写。")
        if approved:
            return ("已修改", "已采纳。相关修改建议已获批准；请根据实际应用结果填写具体修改内容。", location or "待填写。")
        if ignored:
            return ("未修改", "经确认，该项本次不作为修改内容处理；请根据实际情况填写不修改原因。", location or "不适用。")
        if unapproved:
            return ("未批准", "该修改建议已提交审批，但本次未获批准，因此论文暂未据此修改。", location or "不适用。")
        return ("待填写", "待根据论文实际修改情况填写。", location or "待填写。")

    if not approval:
        return ("待填写", "待根据论文实际修改情况填写。", "待填写。")
    if approval.get("cancelled"):
        return ("审批取消", "相关修改审批流程已取消，故本次暂未形成最终修改。", "不适用。")
    return ("待核对审批结果", "已读取审批结果，但尚未建立该专家意见与具体审批项的对应关系；请补充逐条对应关系后填写修改或不修改说明。", "待填写。")


def strip_final_punctuation(text: str) -> str:
    return text.strip().rstrip("。；;")


def clean_explanation(text: str) -> str:
    text = text.strip()
    for prefix in ("已采纳。", "部分采纳。", "已采纳；", "部分采纳；"):
        if text.startswith(prefix):
            return text[len(prefix) :].strip()
    return text


def response_sentence(idx: int, comment: str, status: str, explanation: str, location: str) -> str:
    explanation_text = strip_final_punctuation(clean_explanation(explanation))
    location_text = strip_final_punctuation(location)
    sentence = explanation_text
    if location_text and location_text not in {"不适用", "待填写"}:
        sentence += f"，修改位置为{location_text}"
    return sentence + "。"


def advisor_text(stance: str) -> str:
    if stance == "conditional":
        return """# 导师意见（草稿，供导师确认）

本人已审阅答辩人针对专家评阅意见所作的修改（或不修改）说明及论文修改稿。答辩人已对专家意见进行了认真核对，并对论文中的主要问题作出了相应修改；对于暂未修改或部分修改的内容，答辩人已说明原因。本人原则同意其对专家意见作出的修改或不修改说明。

答辩人仍需在答辩前进一步核对论文格式、参考文献和文字细节。完成上述完善后，本人同意其参加学位论文答辩。
"""
    if stance == "not-agree":
        return """# 导师意见（草稿，供导师确认）

本人已审阅答辩人针对专家评阅意见所作的修改（或不修改）说明及论文修改稿。目前部分专家意见尚未得到充分回应，相关修改说明仍需进一步补充和完善。本人暂不同意答辩人当前版本的修改或不修改说明，暂不同意其以该版本参加学位论文答辩。
"""
    return """# 导师意见（草稿，供导师确认）

本人已审阅答辩人针对专家评阅意见所作的修改（或不修改）说明及论文修改稿。答辩人能够认真对待专家提出的意见，对论文中涉及的文字表述、结构安排、术语记号、参考文献和相关说明等问题进行了逐条核对和相应修改；对于个别未作修改或仅作部分修改的意见，答辩人已结合论文研究内容和实际情况作出说明，理由基本充分。

本人认为，答辩人对专家意见的修改（或不修改）说明较为完整，相关修改能够回应专家意见，论文修改稿已达到申请答辩的要求。本人同意答辩人作出的修改或不修改说明，同意其参加学位论文答辩。
"""


def build_document(
    comments: list[str],
    stance: str,
    title: str | None,
    student: str | None,
    approval: dict | None = None,
    comment_status: dict[int, dict] | None = None,
) -> str:
    lines: list[str] = []
    lines.append("# 针对专家意见的修改（或不修改）说明")
    lines.append("")
    lines.append("本人已认真阅读专家对学位论文提出的评阅意见，并在导师指导下对论文进行了逐条核对和修改。现将针对专家意见的修改（或不修改）情况说明如下。")
    lines.append("")
    sentences: list[str] = []
    for idx, comment in enumerate(comments, 1):
        status, explanation, location = approval_summary(approval or {}, (comment_status or {}).get(idx))
        sentences.append(response_sentence(idx, comment, status, explanation, location))
    lines.append("".join(sentences))
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
    parser.add_argument("--title", help="Accepted for compatibility; not printed by default")
    parser.add_argument("--student", help="Accepted for compatibility; not printed by default")
    parser.add_argument("--approval-json", help="Optional revision-check approval JSON used to set default response status")
    parser.add_argument("--comment-status-json", help="Optional per-comment status mapping JSON; required for approval-aware final wording")
    parser.add_argument(
        "--advisor-stance",
        choices=["agree", "conditional", "not-agree"],
        default="agree",
        help="Advisor-opinion draft stance",
    )
    args = parser.parse_args()

    comments = split_comments(read_comments(args.comments))
    approval = load_approval(args.approval_json)
    comment_status = load_comment_status(args.comment_status_json)
    doc = build_document(comments, args.advisor_stance, args.title, args.student, approval, comment_status)
    if args.out:
        Path(args.out).write_text(doc, encoding="utf-8")
    else:
        print(doc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
