"""Package only deliverable files, with hashes and a ZIP integrity check."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
excluded={'__pycache__','tmp','.venv','.ipynb_checkpoints'}
def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and not excluded.intersection(p.relative_to(ROOT).parts)
        and p.suffix not in {'.pyc','.aux','.out'} and p.name!='final_report.log' and p.name!='FILE_MANIFEST.json')
listing=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files()]
(ROOT/'FILE_MANIFEST.json').write_text(json.dumps({'note':'Manifest excludes itself; source raw CSV is intentionally external','files':listing},indent=2),encoding='utf-8')
target=ROOT.parent/'NullPointer_LendingClub_Midterm_Project.zip'
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
    for p in files()+[ROOT/'FILE_MANIFEST.json']:
        archive.write(p,ROOT.name+'/'+p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    for item in listing:
        data=archive.read(ROOT.name+'/'+item['path'])
        assert hashlib.sha256(data).hexdigest()==item['sha256']
    assert not any(n.endswith('accepted_2007_to_2018Q4.csv') for n in archive.namelist())
digest=hashlib.sha256(target.read_bytes()).hexdigest()
target.with_suffix('.zip.sha256').write_text(digest+'  '+target.name+'\n',encoding='ascii')
print(json.dumps({'zip':str(target),'files':len(listing)+1,'bytes':target.stat().st_size,'sha256':digest,'integrity':'all archive entries and manifest hashes verified'},indent=2))
