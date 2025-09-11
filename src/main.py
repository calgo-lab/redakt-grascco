from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))

from data_handlers.grascco_data_handler import GrasccoDataHandler
from utils.project_utils import ProjectUtils

import json

if __name__ == "__main__":
    project_root: Path = ProjectUtils.get_project_root()
    data_handler = GrasccoDataHandler(project_root)
    eda_summary = data_handler.get_eda_summary()
    with (project_root / "data" / "eda_summary.json").open("w", encoding="utf-8") as f:
        json.dump(eda_summary, f, ensure_ascii=False, indent=4)
