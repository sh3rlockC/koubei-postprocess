#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd


def fail(msg: str):
    raise SystemExit(f'[filter_koubei_submodel] {msg}')


def ensure_file(path: Path, label: str):
    if not path.exists():
        fail(f'{label} 不存在: {path}')
    if path.suffix.lower() not in {'.xlsx', '.xls'}:
        fail(f'{label} 不是 Excel 文件: {path}')


def main():
    ap = argparse.ArgumentParser(description='从双平台口碑汇总中筛选子车型，并拆出 ZJ / DCD raw')
    ap.add_argument('--input', required=True, help='双平台汇总 Excel')
    ap.add_argument('--keyword', required=True, help='子车型关键词，例如 影速')
    ap.add_argument('--output-dir', required=True, help='输出目录')
    ap.add_argument('--model-name', default='', help='大车型名，可选')
    args = ap.parse_args()

    src = Path(args.input)
    outdir = Path(args.output_dir)
    kw = args.keyword.strip()
    label = args.keyword.strip()
    if not kw:
        fail('keyword 不能为空')
    ensure_file(src, 'input')
    outdir.mkdir(parents=True, exist_ok=True)

    xls = pd.ExcelFile(src)
    required = {'ZJ_购车口碑', 'ZJ_试驾口碑', 'DCD_口碑明细'}
    missing = required - set(xls.sheet_names)
    if missing:
        fail(f'双平台汇总缺少 sheet: {sorted(missing)}')
    zj_buy = pd.read_excel(src, sheet_name='ZJ_购车口碑') if 'ZJ_购车口碑' in xls.sheet_names else pd.DataFrame()
    zj_drive = pd.read_excel(src, sheet_name='ZJ_试驾口碑') if 'ZJ_试驾口碑' in xls.sheet_names else pd.DataFrame()
    dcd = pd.read_excel(src, sheet_name='DCD_口碑明细') if 'DCD_口碑明细' in xls.sheet_names else pd.DataFrame()

    if '车型' not in zj_buy.columns and '车型' not in zj_drive.columns:
        fail('ZJ sheet 缺少 车型 列')
    if '评价车型' not in dcd.columns:
        fail('DCD_口碑明细 缺少 评价车型 列')

    zj_buy_f = zj_buy[zj_buy['车型'].astype(str).str.contains(kw, na=False)].copy() if not zj_buy.empty and '车型' in zj_buy.columns else pd.DataFrame()
    zj_drive_f = zj_drive[zj_drive['车型'].astype(str).str.contains(kw, na=False)].copy() if not zj_drive.empty and '车型' in zj_drive.columns else pd.DataFrame()
    dcd_f = dcd[dcd['评价车型'].astype(str).str.contains(kw, na=False)].copy() if not dcd.empty and '评价车型' in dcd.columns else pd.DataFrame()

    if zj_buy_f.empty and zj_drive_f.empty and dcd_f.empty:
        fail(f'没有筛到任何包含关键词“{kw}”的记录')

    summary = outdir / f'{label}_双平台口碑汇总.xlsx'
    zj_raw = outdir / f'ZJ{label}原始口碑.xlsx'
    dcd_raw = outdir / f'DCD{label}口碑.xlsx'

    with pd.ExcelWriter(summary, engine='openpyxl') as writer:
        zj_buy_f.to_excel(writer, sheet_name='ZJ_购车口碑', index=False)
        zj_drive_f.to_excel(writer, sheet_name='ZJ_试驾口碑', index=False)
        dcd_f.to_excel(writer, sheet_name='DCD_口碑明细', index=False)

    with pd.ExcelWriter(zj_raw, engine='openpyxl') as writer:
        zj_buy_f.to_excel(writer, sheet_name='购车口碑', index=False)
        zj_drive_f.to_excel(writer, sheet_name='试驾口碑', index=False)

    with pd.ExcelWriter(dcd_raw, engine='openpyxl') as writer:
        dcd_f.to_excel(writer, sheet_name='口碑明细', index=False)

    print(summary)
    print(zj_raw)
    print(dcd_raw)


if __name__ == '__main__':
    main()
