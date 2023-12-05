# -*- coding: utf-8 -*-
"""Common paths for manipulating datasets and generating figures."""
from pathlib import Path

# Absolute path to the top level of the repository
root = Path(__file__).resolve().parents[2].absolute()

# Absolute path to the `src` folder
src = root / "src"

# Absolute path to the `src/scripts` folder (contains figure/pipeline scripts)
scripts = src / "scripts"

# Absolute path to the `src/figures` folder (contains figure output)
figures = src / "figures"
figures_drafts = src / "figures" / "drafts"

# Constants
const = scripts / "const"

# Absolute path to the `src/data` folder (contains datasets)
data_final = src / "data"
data = root.parent / "data"

# Raw output
data_raw = data / "raw"
# Processed output
data_proc = data / "proc"

# Vertical levels
vert = data / "vert"
# vert = data_final / "vert"