#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd


def fail(msg: str):
    raise SystemExit(f'[build_dual_platform_workbook] {msg}')


def ensure_file(path: Path, label: str):
    if not path.exists():
        fail(f'{label} 不存在: {path}')
    if path.suffix.lower() not in {'.xlsx', '.xls'}:
        fail(f'{label} 不是 Excel 文件: {path}')


def main():
    ap = argparse.ArgumentParser(description='把 ZJ 和 DCD 原始口碑整理成双平台汇总 Excel')
    ap.add_argument('--zj-input', required=True, help='ZJ 合并版 Excel')
    ap.add_argument('--dcd-input', required=True, help='DCD 最终版 Excel')
    ap.add_argument('--output', required=True, help='输出双平台汇总 Excel')
    args = ap.parse_args()

    zj = Path(args.zj_input)
    dcd = Path(args.dcd_input)
    out = Path(args.output)

    ensure_file(zj, 'zj-input')
    ensure_file(dcd, 'dcd-input')

    zj_xls = pd.ExcelFile(zj)
    dcd_xls = pd.ExcelFile(dcd)

    if '购车口碑' not in zj_xls.sheet_names and '试驾口碑' not in zj_xls.sheet_names:
        fail(f'ZJ Excel 缺少 购车口碑/试驾口碑 sheet: {zj}')
    if not dcd_xls.sheet_names:
        fail(f'DCD Excel 没有 sheet: {dcd}')

    zj_buy = pd.read_excel(zj, sheet_name='购车口碑') if '购车口碑' in zj_xls.sheet_names else pd.DataFrame()
    zj_drive = pd.read_excel(zj, sheet_name='试驾口碑') if '试驾口碑' in zj_xls.sheet_names else pd.DataFrame()
    dcd_detail = pd.read_excel(dcd, sheet_name=dcd_xls.sheet_names[0])

    out.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(out, engine='openpyxl') as writer:
        zj_buy.to_excel(writer, sheet_name='ZJ_购车口碑', index=False)
        zj_drive.to_excel(writer, sheet_name='ZJ_试驾口碑', index=False)
        dcd_detail.to_excel(writer, sheet_name='DCD_口碑明细', index=False)

    print(out)


if __name__ == '__main__':
    main()
