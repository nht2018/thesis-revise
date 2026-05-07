# 毕业论文修改 Skill

[中文](README.md) | [English](README.en.md)

`thesis-revision` 是一个面向 LaTeX 学位论文的 agent skill，用于答辩、送审、提交前的非逻辑性修改与复查。它重点处理专家意见、全文语法与一致性、参考文献规范、摘要润色、LaTeX 交叉引用、编译日志和 PDF 呈现问题。

## 功能

- 根据专家意见生成可追踪的最小修改计划。
- 起草中文教务材料，包括“针对专家意见的修改（或不修改）说明”和“导师意见”。
- 进行全文语法和学术表达检查，同时避开 LaTeX、公式和引用噪音。
- 生成项目级 style sheet，用于统一术语、记号、标题、引用和中英文表达。
- 检查由多篇小论文拼接成的学位论文在结构、术语、记号、标题风格、引用和语言风格上的一致性。
- 检查 BibTeX 中的重复文献、大小写保护、正式发表版本优先、期刊/会议名格式、URL、edition 和字段异常。
- 在用户要求联网核验时，辅助检查文献是否存在正式发表版本。
- 润色中英文摘要，并检查摘要与关键词的中英文一致性。
- 诊断 LaTeX/PDF 问题，例如未定义引用、重复自动引用词、算法行号误引、目录页码和参考文献格式。
- 默认采用“先报告再修改”的流程；只有用户明确要求时才直接修改。

## 安装

通常只需要在 agent 中输入：

```text
Install the skill from https://github.com/nht2018/thesis-revise.git as thesis-revision.
```

支持自定义技能/规则/项目指令的主流 coding agent 通常会根据自身机制拉取并启用该 skill，例如 Codex、Claude Code、Cursor CLI 等。

## 使用

示例提示词：

```text
使用 $thesis-revision 检查这篇 LaTeX 毕业论文的非逻辑性问题。
使用 $thesis-revision 根据专家意见给出最小修改计划。
使用 $thesis-revision 根据专家意见起草中文修改说明和导师意见。
使用 $thesis-revision 对全文做语法和学术表达检查。
使用 $thesis-revision 在做一致性修改前生成项目 style sheet。
使用 $thesis-revision 检查参考文献重复和 BibTeX 大小写保护。
使用 $thesis-revision 润色中英文摘要并检查一致性。
```

## 设计原则

- 通用：不假设固定模板、目录结构、学科方向或术语体系。
- 保守：不改变技术结论、定理、算法、实验和核心论断。
- 可追踪：每条专家意见都对应位置、处理方式和验证方法。
- 最小：优先做句子级修改和风格统一，不做大段重写。
- 可验证：修改后编译论文，并检查日志与 PDF 输出。
