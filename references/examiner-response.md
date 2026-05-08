# Examiner Response Materials

Use this guide when the user needs Chinese materials for graduate-school administration after thesis review. These materials should be drafted from verified changes and then reviewed by the student and advisor before submission.

## Required Inputs

- Examiner comments, preferably separated by expert and item number.
- Final modification status for each comment: revised, not revised, partially revised, already addressed, not approved, ignored, or cancelled.
- The `revision-check` approval result when approval was used: approved IDs/items, ignored IDs/items, and cancellation status.
- A per-comment mapping from each examiner comment to its relevant `revision-check` item IDs and final status.
- Verified locations: chapter, section, page, equation/table/figure/algorithm number, or source file line.
- Advisor stance: agree with the revision/non-revision explanation and agree to defense; conditionally agree; or do not agree.

Do not invent completed modifications. If evidence is missing, write "待补充" or ask the user to confirm.

## Approval Mapping Rule

When `revision-check` is used, official wording must follow the approval result:

- `approved_ids` or `approved_items`, after the edits are applied and verified: write a 修改说明, using wording such as `已采纳。论文已在……处修改/补充……。`
- `ignored_ids` or `ignored_items`: write a 不修改说明, using wording such as `经确认，本次暂未按该意见修改，主要原因是……。`
- Items shown in the approval page but not approved: write a 暂未修改说明 or 待确认说明; do not claim they were revised.
- `cancelled: true`: do not draft final "已修改" material. Use a temporary note such as `审批流程已取消，相关修改尚未确认。`
- Items that were already present in the thesis before the approval run may be marked `已在原文体现`, but only after source/PDF verification.

Maintain the mapping from each examiner comment to one or more `revision-check` item IDs. If a comment has both approved and unapproved edits, mark it as `部分修改` and explain both parts. Do not use a global approval JSON alone to mark all comments as revised; approval status must be reconciled per comment.

Optional per-comment status JSON for the helper script:

```json
{
  "1": {
    "approved_ids": ["G1", "L2"],
    "status": "已修改",
    "explanation": "已采纳。论文已在第 X 章第 X 节补充……。",
    "location": "第 X 章第 X 节，第 X 页"
  },
  "2": {
    "ignored_ids": ["G3"],
    "status": "未修改",
    "explanation": "经确认，该项本次不作为修改内容处理，主要原因是……。",
    "location": "不适用"
  }
}
```

Use it with:

```bash
python3 ~/.codex/skills/thesis-revision/scripts/generate_examiner_response.py comments.txt \
  --approval-json /tmp/revision-check-approval.json \
  --comment-status-json comment-status.json \
  --out revision-response.md
```

## Tracking Table

Maintain an internal table before drafting official text:

| 序号 | 专家意见 | 处理状态 | 修改位置 | 修改或不修改说明 | 验证方式 |
| --- | --- | --- | --- | --- | --- |
| 1 | ... | 已修改/未修改/部分修改/已在原文体现/未批准/已忽略/审批取消 | 第 X 章第 X 节，第 X 页 | ... | approval JSON/编译/PDF/源码复查 |

## Official Document 1: 针对专家意见的修改（或不修改）说明

Use this structure for a Chinese official draft:

```markdown
# 针对专家意见的修改（或不修改）说明

本人已认真阅读专家对学位论文提出的评阅意见，并在导师指导下对论文进行了逐条核对和修改。现将针对专家意见的修改（或不修改）情况说明如下。

| 序号 | 专家意见 | 修改（或不修改）说明 | 修改位置 |
| --- | --- | --- | --- |
| 1 | ... | 已采纳。论文已在……处补充/修改……，以……。 | 第 X 章第 X 节，第 X 页 |
| 2 | ... | 经认真核对，暂未按该意见修改，主要原因是……。该处理已与导师沟通确认。 | 不适用/第 X 章第 X 节 |

以上说明均基于论文当前修改稿。本人确认已对专家意见进行了认真核对，并已根据论文实际情况作出相应修改或说明。

答辩人签名：

日期：
```

Recommended wording:

- Revised: `已采纳。论文已在第 X 章第 X 节（第 X 页）补充/修改……，进一步明确……。`
- Partially revised: `部分采纳。论文已在……处补充……；对于……部分，考虑到……，暂未进一步展开。`
- Not revised: `经认真核对，暂未按该意见修改，主要原因是……。该处理不影响论文的主要结论，并已与导师沟通确认。`
- Not approved: `该修改建议已提交审批，但本次未获批准，因此论文暂未据此修改。后续如需处理，可在进一步确认后补充修改。`
- Ignored: `经确认，该项本次不作为修改内容处理，主要原因是……。`
- Cancelled: `相关修改审批流程已取消，故本次暂未形成最终修改。`
- Already addressed: `经核对，原论文已在……处对该问题作出说明。为避免重复，本次未作实质性修改，仅对相关表述进行了……。`

## Official Document 2: 导师意见

Draft advisor text only as a draft for advisor confirmation and signature. The text must explicitly state whether the advisor agrees with the student's revision/non-revision explanation and whether the advisor agrees to the defense.

### Agree to Defense

```markdown
# 导师意见（草稿，供导师确认）

本人已审阅答辩人针对专家评阅意见所作的修改（或不修改）说明及论文修改稿。答辩人能够认真对待专家提出的意见，对论文中涉及的文字表述、结构安排、术语记号、参考文献和相关说明等问题进行了逐条核对和相应修改；对于个别未作修改或仅作部分修改的意见，答辩人已结合论文研究内容和实际情况作出说明，理由基本充分。

本人认为，答辩人对专家意见的修改（或不修改）说明较为完整，相关修改能够回应专家意见，论文修改稿已达到申请答辩的要求。本人同意答辩人作出的修改或不修改说明，同意其参加学位论文答辩。

导师签名：

日期：
```

### Conditional Agreement

```markdown
# 导师意见（草稿，供导师确认）

本人已审阅答辩人针对专家评阅意见所作的修改（或不修改）说明及论文修改稿。答辩人已对专家意见进行了认真核对，并对论文中的主要问题作出了相应修改；对于暂未修改或部分修改的内容，答辩人已说明原因。本人原则同意其对专家意见作出的修改或不修改说明。

答辩人仍需在答辩前进一步核对论文格式、参考文献和文字细节。完成上述完善后，本人同意其参加学位论文答辩。

导师签名：

日期：
```

### Do Not Agree Yet

```markdown
# 导师意见（草稿，供导师确认）

本人已审阅答辩人针对专家评阅意见所作的修改（或不修改）说明及论文修改稿。目前部分专家意见尚未得到充分回应，相关修改说明仍需进一步补充和完善。本人暂不同意答辩人当前版本的修改或不修改说明，暂不同意其以该版本参加学位论文答辩。

导师签名：

日期：
```

## Quality Rules

- Use formal, concise Chinese suitable for administrative submission.
- Avoid overclaiming. Say "基本充分" or "较为完整" unless the advisor explicitly wants stronger wording.
- Keep locations concrete; avoid vague "文中已修改" without chapter/page.
- If the thesis has multiple experts, preserve expert numbering.
- Do not include private deliberation or internal agent notes in the official document.
