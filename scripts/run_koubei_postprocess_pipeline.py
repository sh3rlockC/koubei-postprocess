#!/usr/bin/env python3
import argparse
from pathlib import Path
import subprocess
import sys


def fail(msg: str):
    raise SystemExit(f'[run_koubei_postprocess_pipeline] {msg}')


def ensure_file(path: Path, label: str):
    if not path.exists():
        fail(f'{label} 不存在: {path}')
    if path.suffix.lower() not in {'.xlsx', '.xls'}:
        fail(f'{label} 不是 Excel 文件: {path}')


def ensure_script(path: Path, label: str):
    if not path.exists():
        fail(f'{label} 脚本不存在: {path}')


def run(cmd):
    print('+', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser(description='一键串联口碑后处理：从 ZJ 最终版 + DCD 最终版生成双平台汇总、筛子车型 raw，并继续跑摘要和词云')
    ap.add_argument('--zj-input', required=True, help='ZJ 最终版 Excel')
    ap.add_argument('--dcd-input', required=True, help='DCD 最终版 Excel')
    ap.add_argument('--keyword', required=True, help='子车型关键词，例如 影速')
    ap.add_argument('--output-dir', required=True, help='车型输出目录')
    ap.add_argument('--model-name', default='', help='大车型名，可选')
    ap.add_argument('--summary-name', default='', help='双平台汇总文件名，可选')
    ap.add_argument('--skip-summary', action='store_true', help='跳过摘要生成')
    ap.add_argument('--skip-wordcloud', action='store_true', help='跳过词云生成')
    args = ap.parse_args()

    root = Path(__file__).resolve().parent
    workspace = root.parent.parent.parent
    build_script = root / 'build_dual_platform_workbook.py'
    filter_script = root / 'filter_koubei_submodel.py'
    summary_script = workspace / 'skills' / 'koubei-keyword-summary' / 'skill' / 'scripts' / 'summarize_koubei_excel.py'
    wordcloud_script = workspace / 'skills' / 'koubei-wordcloud' / 'scripts' / 'generate_wordcloud.py'

    if not args.keyword.strip():
        fail('keyword 不能为空')
    ensure_file(Path(args.zj_input), 'zj-input')
    ensure_file(Path(args.dcd_input), 'dcd-input')
    ensure_script(build_script, 'build_dual_platform_workbook')
    ensure_script(filter_script, 'filter_koubei_submodel')
    if not args.skip_summary:
        ensure_script(summary_script, 'summarize_koubei_excel')
    if not args.skip_wordcloud:
        ensure_script(wordcloud_script, 'generate_wordcloud')

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    summary_name = args.summary_name or (f'{args.model_name}_双平台口碑汇总.xlsx' if args.model_name else '双平台口碑汇总.xlsx')
    summary_path = outdir / summary_name
    sub_dir = outdir / args.keyword
    sub_summary = sub_dir / f'{args.keyword}_双平台口碑摘要.xlsx'
    zj_raw = sub_dir / f'ZJ{args.keyword}原始口碑.xlsx'
    dcd_raw = sub_dir / f'DCD{args.keyword}口碑.xlsx'

    run([
        sys.executable, str(build_script),
        '--zj-input', args.zj_input,
        '--dcd-input', args.dcd_input,
        '--output', str(summary_path),
    ])

    run([
        sys.executable, str(filter_script),
        '--input', str(summary_path),
        '--keyword', args.keyword,
        '--output-dir', str(sub_dir),
        '--model-name', args.model_name,
    ])

    if not args.skip_summary:
        run([
            sys.executable, str(summary_script),
            '--autohome-input', str(zj_raw),
            '--dcd-input', str(dcd_raw),
            '--output', str(sub_summary),
            '--model-name', args.keyword,
        ])

    if not args.skip_wordcloud:
        if sub_summary.exists() and not args.skip_summary:
            run([
                sys.executable, str(wordcloud_script),
                '--input', str(sub_summary),
                '--output-dir', str(sub_dir),
                '--model-name', args.keyword,
            ])
        else:
            run([
                sys.executable, str(wordcloud_script),
                '--autohome-input', str(zj_raw),
                '--dcd-input', str(dcd_raw),
                '--output-dir', str(sub_dir),
                '--model-name', args.keyword,
            ])

    print('DONE')
    print(summary_path)
    print(sub_dir)


if __name__ == '__main__':
    main()
