from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.reporting import generate
generate()
print('Reports and LaTeX source generated from computed JSON outputs.')
