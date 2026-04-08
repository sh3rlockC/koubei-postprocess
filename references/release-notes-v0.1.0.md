# koubei-postprocess v0.1.0

首个可用版本，聚焦口碑采集后的标准化后处理流程。

## 包含能力
- 合并 ZJ / DCD 断点前后 Excel
- 生成双平台汇总 Excel
- 从双平台汇总筛选子车型
- 一键串联：双平台汇总 → 子车型 raw → 摘要 → 词云
- 基础参数校验与更清晰的错误提示

## 附带脚本
- `merge_koubei_excels.py`
- `build_dual_platform_workbook.py`
- `filter_koubei_submodel.py`
- `run_koubei_postprocess_pipeline.py`

## 推荐命名约定
- `ZJ口碑_车型_最终版.xlsx`
- `DCD口碑_车型_最终版.xlsx`

## 后续可继续增强
- 更细的统计与校验输出
- 更多子车型筛选规则
- 更正式的 package / release 自动化
