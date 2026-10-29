"""One-command full rebuild; requires raw data, dependencies and a TeX compiler."""
from pathlib import Path
import argparse,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);ap.add_argument('--tectonic');args=ap.parse_args()
steps=[['scripts/run_all.py','--data',str(Path(args.data).resolve())],
       ['scripts/generate_summary_figures.py'],['scripts/generate_reports.py'],
       ['scripts/create_viva.py'],['scripts/create_notebooks.py'],['scripts/execute_notebooks.py'],
       ['scripts/compile_report.py']+(['--tectonic',str(Path(args.tectonic).resolve())] if args.tectonic else []),
       ['scripts/validate_project.py']]
for step in steps:
    print('Running '+' '.join(step),flush=True)
    subprocess.run([sys.executable]+step,cwd=ROOT,check=True)
print('Rebuild completed. Inspect the regenerated PDF visually before submission.')
