# 毕业论文修改 Skill

[English](README.md) | [中文](README.zh-CN.md)

`thesis-revision` 是一个面向 LaTeX 学位论文的 agent skill，用于答辩、送审、提交前的非逻辑性修改与复查。它重点处理专家意见、全文语法与一致性、参考文献规范、摘要润色、LaTeX 交叉引用、编译日志和 PDF 呈现问题。

## 功能

- 根据专家意见生成可追踪的最小修改计划。
- 进行全文语法和学术表达检查，同时避开 LaTeX、公式和引用噪音。
- 检查由多篇小论文拼接成的学位论文在结构、术语、记号、标题风格、引用和语言风格上的一致性。
- 检查 BibTeX 中的重复文献、大小写保护、正式发表版本优先、期刊/会议名格式、URL、edition 和字段异常。
- 润色中英文摘要，并检查摘要与关键词的中英文一致性。
- 诊断 LaTeX/PDF 问题，例如未定义引用、重复自动引用词、算法行号误引、目录页码和参考文献格式。
- 默认采用“先报告再修改”的流程；只有用户明确要求时才直接修改。

## 安装

将本仓库安装或复制到 agent skills 目录：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/nht2018/thesis-revise.git ~/.codex/skills/thesis-revision
```

如果本地已安装：

```bash
cd ~/.codex/skills/thesis-revision
git pull
```

## 使用

示例提示词：

```text
使用 $thesis-revision 检查这篇 LaTeX 毕业论文的非逻辑性问题。
使用 $thesis-revision 根据专家意见给出最小修改计划。
使用 $thesis-revision 对全文做语法和学术表达检查。
使用 $thesis-revision 检查参考文献重复和 BibTeX 大小写保护。
使用 $thesis-revision 润色中英文摘要并检查一致性。
```

## 辅助脚本

本 skill 包含启发式扫描脚本。它们只作为辅助工具，不能替代人工审查。

```bash
python3 scripts/scan_latex_thesis.py /path/to/thesis --pdf /path/to/thesis.pdf
python3 scripts/check_bibliography.py /path/to/references.bib
```

## 仓库结构

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── bibliography-checklist.md
│   ├── consistency-checklist.md
│   ├── grammar-checklist.md
│   ├── latex-pdf-checklist.md
│   └── revision-workflow.md
└── scripts/
    ├── check_bibliography.py
    └── scan_latex_thesis.py
```

## 设计原则

- 通用：不假设固定模板、目录结构、学科方向或术语体系。
- 保守：不改变技术结论、定理、算法、实验和核心论断。
- 可追踪：每条专家意见都对应位置、处理方式和验证方法。
- 最小：优先做句子级修改和风格统一，不做大段重写。
- 可验证：修改后编译论文，并检查日志与 PDF 输出。
