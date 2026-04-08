# koubei-postprocess workflow

## 目标
把口碑采集后的整理动作拆成 3 个稳定步骤：

1. 合并 ZJ 断点前后 Excel
2. 生成双平台汇总 Excel
3. 从汇总里筛子车型并给下游准备输入

## Step 1. 合并 ZJ
输入：
- 续跑主文件
- 可选诊断页 / 补抓页文件

规则：
- 以续跑主文件为主
- 诊断页 / 补抓页按 `来源链接` 覆盖或补充
- 输出合并版

## Step 2. 双平台汇总
输入：
- ZJ 合并版
- DCD 最终版

输出：
- 双平台汇总 Excel
- sheet 建议固定为 `ZJ_购车口碑`、`ZJ_试驾口碑`、`DCD_口碑明细`

## Step 3. 子车型筛选
输入：
- 双平台汇总 Excel
- 子车型关键词（例如“影速”）

规则：
- ZJ 按 `车型` contains 筛
- DCD 按 `评价车型` contains 筛
- 导出子车型汇总、ZJ raw、DCD raw

## Step 4. 下游
把子车型 raw 交给：
- 摘要 skill
- 词云 skill
