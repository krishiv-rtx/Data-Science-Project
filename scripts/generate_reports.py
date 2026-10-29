from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.reporting import generate
generate()
<<<<<<< HEAD
from src.report_presentation import refine
refine()
from src.reader_guide import apply
apply()
from src.report_math import annotate
annotate()
=======
>>>>>>> origin/main
print('Reports and LaTeX source generated from computed JSON outputs.')
