from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "src"))

from data_handlers.grascco_data_handler import GrasccoDataHandler
from flair.data import Corpus, Dictionary
from flair.datasets import ColumnCorpus
from flair.embeddings import TokenEmbeddings, TransformerWordEmbeddings
from utils.project_utils import ProjectUtils

import os


def fine_tune():

    project_root: Path = ProjectUtils.get_project_root()

    model_checkpoints_root_dir = os.environ.get("MODEL_CHECKPOINTS_ROOT_DIR", None)
    model_checkpoints_root_dir = Path(model_checkpoints_root_dir) if model_checkpoints_root_dir else Path.home() / "model_checkpoints"
    data_fold_k_value = os.environ.get("DATA_FOLD_K_VALUE", None)
    data_fold_k_value = int(data_fold_k_value) if data_fold_k_value else 1
    learning_rate = os.environ.get("LEARNING_RATE", None)
    learning_rate = float(learning_rate) if learning_rate else 6e-5
    max_epochs = os.environ.get("MAX_EPOCHS", None)
    max_epochs = int(max_epochs) if max_epochs else 15
    mini_batch_size = os.environ.get("MINI_BATCH_SIZE", None)
    mini_batch_size = int(mini_batch_size) if mini_batch_size else 2

    data_handler = GrasccoDataHandler(project_root)
    datasetdict = data_handler.get_train_dev_test_datasetdict(data_fold_k_value)
    train_df = datasetdict["train"].to_pandas()
    dev_df = datasetdict["dev"].to_pandas()
    test_df = datasetdict["test"].to_pandas()
    sample_size = len(train_df) + len(dev_df) + len(test_df)

    print(f"model_checkpoints_root_dir: {model_checkpoints_root_dir}")
    print(f"data_fold_k_value: {data_fold_k_value}")
    print(f"sample_size: {sample_size}")
    print(f"learning_rate: {learning_rate:.0e}".replace('e-0', 'e-'))
    print(f"mini_batch_size: {mini_batch_size}")
    print(f"max_epochs: {max_epochs}")

    data_dir_path = model_checkpoints_root_dir / "grascco" / "ner" / "deepset-gelectra-large"
    data_dir_path = data_dir_path / "additional-embeddings-none" / "use-context"
    data_dir_path =  data_dir_path / f"sample-size-{sample_size}" / f"data-fold-{data_fold_k_value}"
    data_dir_path.mkdir(parents=True, exist_ok=True)

    train_text = train_df.bioes_text.str.cat(sep="\n")
    dev_text = dev_df.bioes_text.str.cat(sep="\n")
    test_text = test_df.bioes_text.str.cat(sep="\n")
    with (data_dir_path / "train.txt").open("w", encoding="utf-8") as writer:
        writer.write(train_text)
    with (data_dir_path / "dev.txt").open("w", encoding="utf-8") as writer:
        writer.write(dev_text)
    with (data_dir_path / "test.txt").open("w", encoding="utf-8") as writer:
        writer.write(test_text)

    corpus: Corpus = ColumnCorpus(data_dir_path, {0: 'text', 1: 'ner'})
    label_dict: Dictionary = corpus.make_label_dictionary(label_type="ner")
    print(f"{label_dict}")

    model_dir_path = data_dir_path / f"learning-rate-{learning_rate:.0e}".replace('e-0', 'e-')
    model_dir_path = model_dir_path / f"max-epochs-{max_epochs}"
    model_dir_path = model_dir_path / f"mini-batch-size-{mini_batch_size}"
    os.makedirs(model_dir_path, exist_ok=True)

    
if __name__ == "__main__":
    fine_tune()