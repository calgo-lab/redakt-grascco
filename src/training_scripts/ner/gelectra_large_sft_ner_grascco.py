from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

import os


def fine_tune():
    flair_cache_root = os.environ.get("FLAIR_CACHE_ROOT", None)
    print(f"FLAIR_CACHE_ROOT: {flair_cache_root}")

if __name__ == "__main__":
    fine_tune()