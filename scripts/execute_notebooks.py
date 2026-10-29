"""Execute plain-Python notebook cells in fresh processes, recording real outputs.

This lightweight runner supports these notebooks (no magics). For arbitrary
Jupyter notebooks use nbclient/Jupyter instead. Never fabricates execution counts.
"""
from pathlib import Path
import argparse,contextlib,io,json,os,subprocess,sys,traceback
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--worker',type=Path);args=ap.parse_args()
if args.worker:
    path=args.worker; notebook=json.loads(path.read_text(encoding='utf-8'))
    env={'__name__':'__main__'};count=0;os.chdir(ROOT);sys.path.insert(0,str(ROOT))
    for cell in notebook['cells']:
        if cell['cell_type']!='code':continue
        count+=1;stream=io.StringIO();cell['execution_count']=count
        try:
            with contextlib.redirect_stdout(stream):exec(compile(''.join(cell['source']),str(path),'exec'),env)
            cell['outputs']=[{'output_type':'stream','name':'stdout','text':stream.getvalue().splitlines(keepends=True)}] if stream.getvalue() else []
        except Exception as error:
            cell['outputs']=[{'output_type':'error','ename':type(error).__name__,'evalue':str(error),'traceback':traceback.format_exc().splitlines()}]
            path.write_text(json.dumps(notebook,indent=2),encoding='utf-8');raise
    path.write_text(json.dumps(notebook,indent=2),encoding='utf-8')
    print(path.name+f': {count} code cells executed')
else:
    logs=[]
    for path in sorted((ROOT/'notebooks').glob('*.ipynb')):
        result=subprocess.run([sys.executable,__file__,'--worker',str(path)],capture_output=True,text=True,cwd=ROOT)
        logs.append(result.stdout+result.stderr)
        if result.returncode:
            (ROOT/'outputs/logs/notebooks.log').write_text('\n'.join(logs),encoding='utf-8');raise SystemExit(result.returncode)
    (ROOT/'outputs/logs/notebooks.log').write_text('\n'.join(logs),encoding='utf-8');print('\n'.join(logs))
