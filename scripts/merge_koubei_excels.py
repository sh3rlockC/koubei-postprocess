#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys
import pandas as pd


def fail(msg: str):
    raise SystemExit(f'[merge_koubei_excels] {msg}')


def ensure_file(path: Path, label: str):
    if not path.exists():
        fail(f'{label} 不存在: {path}')
    if path.suffix.lower() not in {'.xlsx', '.xls'}:
        fail(f'{label} 不是 Excel 文件: {path}')


def merge_sheet(base_df: pd.DataFrame, patch_df: pd.DataFrame) -> pd.DataFrame:
    if patch_df is None or patch_df.empty:
        return base_df.copy()
    for col in base_df.columns:
        if col not in patch_df.columns:
            patch_df[col] = pd.NA
    patch_df = patch_df[base_df.columns]
    merged = pd.concat([base_df, patch_df], ignore_index=True)
    if '来源链接' in merged.columns:
        merged = merged.drop_duplicates(subset=['来源链接'], keep='last')
    else:
        merged = merged.drop_duplicates(keep='last')
    return merged


def main():
    ap = argparse.ArgumentParser(description='按来源链接合并口碑 Excel（适合 ZJ 续跑 / 诊断页 / 补抓页）')
    ap.add_argument('--base', required=True, help='主 Excel，一般为续跑结果')
    ap.add_argument('--patch', action='append', default=[], help='补丁 Excel，可重复传入多个')
    ap.add_argument('--output', required=True, help='输出 Excel')
    args = ap.parse_args()

    base = Path(args.base)
    out = Path(args.output)
    patches = [Path(p) for p in args.patch]

    ensure_file(base, 'base')
    if not patches:
        fail('至少需要一个 --patch')
    for p in patches:
        ensure_file(p, 'patch')

    xls = pd.ExcelFile(base)
    if not xls.sheet_names:
        fail(f'base Excel 没有 sheet: {base}')
    merged = {sheet: pd.read_excel(base, sheet_name=sheet) for sheet in xls.sheet_names}

    for patch in patches:
        px = pd.ExcelFile(patch)
        for sheet in merged.keys():
            patch_df = pd.read_excel(patch, sheet_name=sheet) if sheet in px.sheet_names else pd.DataFrame(columns=merged[sheet].columns)
            merged[sheet] = merge_sheet(merged[sheet], patch_df)

    out.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(out, engine='openpyxl') as writer:
        for sheet, df in merged.items():
            df.to_excel(writer, sheet_name=sheet, index=False)

    print(out)


if __name__ == '__main__':
    main()
