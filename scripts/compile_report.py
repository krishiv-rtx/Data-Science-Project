"""Compile the supplied-template adaptation, then verify the eight-page limit."""
from pathlib import Path
import shutil,subprocess,json,argparse
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--tectonic');args=parser.parse_args()
compiler=shutil.which('pdflatex')
if not compiler and not args.tectonic:
    raise SystemExit('pdflatex unavailable. Install MiKTeX/TeX Live, then rerun python scripts/compile_report.py. No PDF success is claimed.')
commands=[[str(Path(args.tectonic).resolve()),'--keep-logs','final_report.tex']] if args.tectonic else [[compiler,'-interaction=nonstopmode','-halt-on-error','final_report.tex']]*2
for command in commands:
    result=subprocess.run(command,cwd=ROOT/'reports',capture_output=True,text=True)
    (ROOT/'outputs/logs/latex.log').write_text(result.stdout+'\n'+result.stderr,encoding='utf-8')
    if result.returncode:raise SystemExit('Compilation failed; inspect outputs/logs/latex.log')
from pypdf import PdfReader
pages=len(PdfReader(ROOT/'reports/final_report.pdf').pages)
if pages>8:raise SystemExit(f'Report has {pages} pages; maximum 8')
(ROOT/'outputs/pdf_validation.json').write_text(json.dumps({'compiled':True,'pages':pages}),encoding='utf-8')
print(f'Compiled and checked: {pages} pages')
