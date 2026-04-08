---
name: koubei-postprocess
description: 对汽车之家与懂车帝口碑采集产物做后处理编排，包括双平台汇总、断点续跑结果合并、子车型筛选、为摘要与词云准备标准输入。适用于用户要求“把 ZJ 和 DCD 整理到一起”“合并断点前后 Excel”“筛出某个子车型版本”“生成双平台汇总后继续做摘要/词云”等场景。
---

# 口碑后处理与编排

目标：把口碑采集后的整理动作标准化，避免每次手工拼 Excel、手工筛子车型、手工给摘要与词云准备输入。

## 1. 适用范围

本 skill 负责后处理，不负责重新采集页面。

适合处理：
- ZJ 断点前后 Excel 合并
- DCD 修复版 / 最终版整理
- 双平台汇总 Excel 生成
- 从双平台汇总里筛子车型
- 为 `koubei-keyword-summary` 和 `koubei-wordcloud` 准备标准输入

不适合处理：
- 新的网页采集
- 浏览器诊断
- 直接跑汽车之家 / 懂车帝页面

## 2. 推荐产物结构

```text
<车型目录>/
  ZJ口碑_车型_最终版.xlsx
  DCD口碑_车型_最终版.xlsx
  车型_双平台口碑汇总.xlsx
  <子车型名>/
    <子车型名>_双平台口碑汇总.xlsx
    ZJ<子车型名>原始口碑.xlsx
    DCD<子车型名>口碑.xlsx
    <子车型名>_双平台口碑摘要.xlsx
    <子车型名>_优点词云.png
    <子车型名>_槽点词云.png
```

## 3. 工作流

### A. 合并 ZJ / DCD 断点前后结果

#### ZJ
- 优先以续跑结果为主
- 若存在诊断页 / 补抓页，按 `来源链接` 去重合并
- 推荐最终统一命名为 `ZJ口碑_车型_最终版.xlsx`

#### DCD
- 若存在修复版 / 补抓版 / 多轮导出结果，同样按 `来源链接` 去重合并
- 推荐最终统一命名为 `DCD口碑_车型_最终版.xlsx`
- 不要简单拼接多个 DCD Excel，避免重复口碑残留

### B. 生成双平台汇总

默认输出这些 sheet：
- `ZJ_购车口碑`
- `ZJ_试驾口碑`
- `DCD_口碑明细`

### C. 筛选子车型

- 汽车之家按 `车型` 包含关键词筛选
- 懂车帝按 `评价车型` 包含关键词筛选
- 输出子车型汇总 + 双 raw

### D. 给下游准备输入

产出后优先把：
- `ZJ<子车型名>原始口碑.xlsx`
- `DCD<子车型名>口碑.xlsx`

交给：
- `koubei-keyword-summary`
- `koubei-wordcloud`

## 4. 规则

- 默认按 `来源链接` 去重，不要简单拼接
- 子车型任务优先从双平台汇总筛，不优先重跑采集
- 整车型与子车型结果分目录存放，避免混放
- 产物命名要直观，优先让人一眼看懂用途

## 5. 参考资料

需要统一流程时，优先查看：
- `/Users/xyc/.openclaw/workspace/docs/system/KOUBEI-TASK-SOP.md`
- `/Users/xyc/.openclaw/workspace/docs/system/KOUBEI-WORKFLOW-CHECKLIST.md`

## 6. 附带脚本

已提供：
- `scripts/merge_koubei_excels.py`
- `scripts/build_dual_platform_workbook.py`
- `scripts/filter_koubei_submodel.py`
- `scripts/run_koubei_postprocess_pipeline.py`

如果是标准后处理任务，优先直接调用脚本，而不是手工拼 Excel。

### 示例 1：合并 ZJ 续跑与补抓结果

```bash
python3 skills/koubei-postprocess/scripts/merge_koubei_excels.py \
  --base /path/to/ZJ车型原始口碑_续跑.xlsx \
  --patch /path/to/ZJ车型_诊断页17-18.xlsx \
  --output /path/to/ZJ车型原始口碑_合并版.xlsx
```

### 示例 2：合并 DCD 修复版 / 补抓版

```bash
python3 skills/koubei-postprocess/scripts/merge_koubei_excels.py \
  --base /path/to/DCD口碑_车型_主结果.xlsx \
  --patch /path/to/DCD口碑_车型_补抓版.xlsx \
  --output /path/to/DCD口碑_车型_最终版.xlsx
```

### 示例 3：生成双平台汇总

```bash
python3 skills/koubei-postprocess/scripts/build_dual_platform_workbook.py \
  --zj-input /path/to/ZJ口碑_车型_最终版.xlsx \
  --dcd-input /path/to/DCD口碑_车型_最终版.xlsx \
  --output /path/to/车型_双平台口碑汇总.xlsx
```

### 示例 4：筛选子车型

```bash
python3 skills/koubei-postprocess/scripts/filter_koubei_submodel.py \
  --input /path/to/车型_双平台口碑汇总.xlsx \
  --keyword 影速 \
  --output-dir /path/to/车型目录/影速
```

### 示例 5：一键从 ZJ + DCD 到子车型 raw

```bash
python3 skills/koubei-postprocess/scripts/run_koubei_postprocess_pipeline.py \
  --zj-input /path/to/ZJ口碑_车型_最终版.xlsx \
  --dcd-input /path/to/DCD口碑_车型_最终版.xlsx \
  --keyword 影速 \
  --output-dir /path/to/车型目录 \
  --model-name 传祺GS3
```
