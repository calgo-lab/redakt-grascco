from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from data_handlers.grascco_data_handler import GrasccoDataHandler
from utils.project_utils import ProjectUtils

if __name__ == "__main__":

    project_root: Path = ProjectUtils.get_project_root()
    data_handler = GrasccoDataHandler(project_root)
    eda_summary = data_handler.get_eda_summary()
    [print(item) for item in eda_summary["label_wise_entity_count"].items()]