# koubei-postprocess

口碑采集后的后处理 workflow skill。

负责：
- 合并 ZJ / DCD 断点前后 Excel
- 生成双平台汇总
- 从双平台汇总筛子车型
- 串联摘要与词云

## 典型场景

### 1. 合并 ZJ 续跑与补抓结果

```bash
python3 skills/koubei-postprocess/scripts/merge_koubei_excels.py \
  --base /path/to/ZJ口碑_车型_主结果.xlsx \
  --patch /path/to/ZJ口碑_车型_补抓版.xlsx \
  --output /path/to/ZJ口碑_车型_最终版.xlsx
```

### 2. 合并 DCD 主结果与补抓版

```bash
python3 skills/koubei-postprocess/scripts/merge_koubei_excels.py \
  --base /path/to/DCD口碑_车型_主结果.xlsx \
  --patch /path/to/DCD口碑_车型_补抓版.xlsx \
  --output /path/to/DCD口碑_车型_最终版.xlsx
```

### 3. 生成双平台汇总

```bash
python3 skills/koubei-postprocess/scripts/build_dual_platform_workbook.py \
  --zj-input /path/to/ZJ口碑_车型_最终版.xlsx \
  --dcd-input /path/to/DCD口碑_车型_最终版.xlsx \
  --output /path/to/车型_双平台口碑汇总.xlsx
```

### 4. 从双平台汇总筛子车型

```bash
python3 skills/koubei-postprocess/scripts/filter_koubei_submodel.py \
  --input /path/to/车型_双平台口碑汇总.xlsx \
  --keyword 影速 \
  --output-dir /path/to/车型目录/影速
```

### 5. 一键跑完整后处理链

```bash
python3 skills/koubei-postprocess/scripts/run_koubei_postprocess_pipeline.py \
  --zj-input /path/to/ZJ口碑_车型_最终版.xlsx \
  --dcd-input /path/to/DCD口碑_车型_最终版.xlsx \
  --keyword 影速 \
  --output-dir /path/to/车型目录 \
  --model-name 传祺GS3
```

## 默认输出

```text
<车型目录>/
  车型_双平台口碑汇总.xlsx
  <子车型名>/
    <子车型名>_双平台口碑汇总.xlsx
    ZJ<子车型名>原始口碑.xlsx
    DCD<子车型名>口碑.xlsx
    <子车型名>_双平台口碑摘要.xlsx
    <子车型名>_优点词云.png
    <子车型名>_槽点词云.png
    <子车型名>_词云词项清单.xlsx
```

## 约定

- ZJ / DCD 最终交付统一推荐命名为“最终版”
- 合并默认按 `来源链接` 去重
- 子车型优先从双平台汇总筛，不优先重跑采集

## Changelog & Releases

- User-visible changes are tracked in [`CHANGELOG.md`](./CHANGELOG.md).
- For a new release, update the `Unreleased` section first, then cut the versioned release.
- GitHub Release notes should match the same user-visible changes, not just raw commit history.

