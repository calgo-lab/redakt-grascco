from datasets import Dataset, DatasetDict
from pandas import DataFrame
from pathlib import Path
from sklearn.model_selection import KFold
from typing import Any, List, Dict, Set, Tuple

import json
import numpy as np
import pandas as pd
import random

class GrasccoDataHandler:
    """
    Data handler for the GraSCCo dataset.
    """
    def __init__(self, project_root: Path, data_dir: Path = None):
        """
        Initialize the GrasccoDataHandler with the path to the data directory.
        The path to all the GraSCCo PHI annotation .json files exports created 
        with the INCEpTION annotation platform.
        """
        self._project_root = project_root
        self._data_root = project_root / "data"
        if data_dir:
            self._data_dir = data_dir
        else:
            self._data_dir = self._data_root / "raw" / "11502329" / "grascco_phi_annotation_json"
        self._json_data_items: List[Dict[str, Any]] = list()
        self._json_data_required_key_dict: Dict[str, str] = {
            "feature_structures": "%FEATURE_STRUCTURES",
            "type": "%TYPE",
            "document_meta_data": "de.tudarmstadt.ukp.dkpro.core.api.metadata.type.DocumentMetaData",
            "sofa": "uima.cas.Sofa",
            "sentence": "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence",
            "token": "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token",
            "phi": "webanno.custom.PHI",
            "document_title": "documentTitle",
            "sofa_string": "sofaString",
            "begin": "begin",
            "end": "end",
            "kind": "kind",
            "label": "label"
        }
        self._ner_data_items: Dict[str, Any] = dict()
        self._eda_summary: Dict[str, Any] = dict()
        self._ner_dataframe: DataFrame = None
        self._load_json_files()

    def _load_json_files(self):
        """
        Load all JSON files from the data directory.
        """
        json_data_path_dict: Dict[str, Dict[str, Any]] = dict()
        for json_file in self._data_dir.glob("*.json"):
            with json_file.open("r", encoding="utf-8") as f:
                data: Dict[str, Any] = json.load(f)
                json_data_path_dict[json_file.name] = data
        self._json_data_items = [v for k, v in sorted(json_data_path_dict.items())]

    def _extract_ner_data(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract NER relevant data from a single dict object extracted from corresponding JSON file.
        :param json_data: The JSON data dictionary object to process.
        :return: The NER data dictionary object.
        """
        ner_data: Dict[str, Any] = dict()
        
        document_title: str = ""
        document_text: str = ""
        sentences: List[Dict[str, Any]] = list()
        tokens: List[Dict[str, Any]] = list()
        entities: List[Dict[str, Any]] = list()

        features_structures = json_data[self._json_data_required_key_dict["feature_structures"]]
        
        for item in features_structures:
            if item[self._json_data_required_key_dict["type"]] == self._json_data_required_key_dict["document_meta_data"]:
                document_title = item[self._json_data_required_key_dict["document_title"]]
            elif item[self._json_data_required_key_dict["type"]] == self._json_data_required_key_dict["sofa"]:
                document_text = item[self._json_data_required_key_dict["sofa_string"]]
            elif item[self._json_data_required_key_dict["type"]] == self._json_data_required_key_dict["sentence"]:
                sentence: Dict[str, Any] = {
                    "begin": item[self._json_data_required_key_dict["begin"]],
                    "end": item[self._json_data_required_key_dict["end"]]
                }
                sentences.append(sentence)
            elif item[self._json_data_required_key_dict["type"]] == self._json_data_required_key_dict["token"]:
                token: Dict[str, Any] = {
                    "begin": item[self._json_data_required_key_dict["begin"]],
                    "end": item[self._json_data_required_key_dict["end"]]
                }
                tokens.append(token)
            elif item[self._json_data_required_key_dict["type"]] == self._json_data_required_key_dict["phi"]:
                label: str = ""
                if self._json_data_required_key_dict["kind"] in item:
                    label = item[self._json_data_required_key_dict["kind"]]
                elif self._json_data_required_key_dict["label"] in item:
                    label = item[self._json_data_required_key_dict["label"]]
                entity: Dict[str, Any] = {
                    "begin": item[self._json_data_required_key_dict["begin"]],
                    "end": item[self._json_data_required_key_dict["end"]],
                    "label": label
                }
                entities.append(entity)

        [s.update({"text": document_text[s["begin"]:s["end"]]}) for s in sentences]
        [t.update({"text": document_text[t["begin"]:t["end"]]}) for t in tokens]
        [e.update({"text": document_text[e["begin"]:e["end"]]}) for e in entities]

        ner_data["document_title"] = document_title
        ner_data["document_text"] = document_text
        ner_data["sentences"] = sentences
        ner_data["tokens"] = tokens
        ner_data["entities"] = entities

        if ner_data["document_title"] == "Queisser.txt":
            ner_data = self._fix_queisser_missing_age_entity_label(ner_data)

        return ner_data
    
    def _fix_queisser_missing_age_entity_label(self, ner_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fix missing age entity label in the NER data of Queisser.txt_phi.json file.
        :param ner_data: The NER data to fix.
        :return: The fixed NER data.
        """
        entities: List[Dict[str, Any]] = ner_data["entities"]
        fixed_entities: List[Dict[str, Any]] = list()
        if ner_data["document_title"] == "Queisser.txt":
            for entity in entities:
                if entity["begin"] == 1219 and entity["end"] == 1221 and entity["text"] == "49":
                    entity["label"] = "AGE"
                fixed_entities.append(entity)
        ner_data["entities"] = fixed_entities
        return ner_data

    def _build_ner_data_items(self) -> None:
        """
        Collect NER relevant data from the dict objects loaded for all JSON data files.
        """
        ner_data_list: List[Dict[str, Any]] = list()
        for json_data in self._json_data_items:
            ner_data = self._extract_ner_data(json_data)
            ner_data_list.append(ner_data)
        self._ner_data_items = ner_data_list

    def get_ner_data_items(self) -> List[Dict[str, Any]]:
        """
        Retrieve the list of NER data dictionaries.
        :return: A list of NER data dictionaries.
        """
        if not self._ner_data_items:
            self._build_ner_data_items()
        return self._ner_data_items
    
    def _build_bioes_text_for_ner_data_item(self, ner_data: Dict[str, Any]) -> str:
        """
        Prepare the BIOES formatted text from the NER data dictionary object.
        :param ner_data: The NER data dictionary object to process.
        :return: The BIOES formatted text.
        """
        tokens: List[Dict[str, Any]] = ner_data.get("tokens", list())
        entities: List[Dict[str, Any]] = ner_data.get("entities", list())

        [t.update({"bioes_tag": "O"}) for t in tokens]

        for entity in entities:
            begin = entity.get("begin", 0)
            end = entity.get("end", 0)
            label = entity.get("label", "")
            tokens_within_entity_boundary: List[Dict[str, Any]] = list()
            for token in tokens:
                if token["begin"] >= begin and token["end"] <= end:
                    tokens_within_entity_boundary.append(token)
            if tokens_within_entity_boundary:
                if len(tokens_within_entity_boundary) == 1:
                    tokens_within_entity_boundary[0]["bioes_tag"] = f"S-{label}"
                else:
                    tokens_within_entity_boundary[0]["bioes_tag"] = f"B-{label}"
                    for i in range(1, len(tokens_within_entity_boundary) - 1):
                        tokens_within_entity_boundary[i]["bioes_tag"] = f"I-{label}"
                    tokens_within_entity_boundary[-1]["bioes_tag"] = f"E-{label}"
        
        return "\n".join(f"{token["text"]} {token["bioes_tag"]}" for token in tokens)
    
    def _build_eda_summary(self, rare_label_entity_count_threshold=10) -> None:
        """
        Build an exploratory data analysis (EDA) summary of the NER data.
        :param rare_label_entity_count_threshold: Threshold to consider a label as rare.
        """
        ner_data_items = self.get_ner_data_items()

        total_sentences: int = 0
        total_tokens: int = 0
        total_entities: int = 0
        file_wise_sentence_token_entity_count: Dict[str, Tuple[int, int, int]] = dict()
        label_wise_entity_count: Dict[str, int] = dict()
        file_wise_label_wise_entity_count: Dict[str, Dict[str, int]] = dict()
        
        for item in ner_data_items:
            document_title = item.get("document_title", "")
            sentence_count = len(item.get("sentences", []))
            total_sentences += sentence_count
            token_count = len(item.get("tokens", []))
            total_tokens += token_count
            entities = item.get("entities", [])
            entity_count = len(entities)
            total_entities += entity_count
            file_wise_sentence_token_entity_count[document_title] = (sentence_count, token_count, entity_count)
            for entity in entities:
                label = entity.get("label", "")
                if label:
                    label_wise_entity_count[label] = label_wise_entity_count.get(label, 0) + 1
                    if document_title not in file_wise_label_wise_entity_count:
                        file_wise_label_wise_entity_count[document_title] = dict()
                    if label not in file_wise_label_wise_entity_count[document_title]:
                        file_wise_label_wise_entity_count[document_title][label] = 0
                    file_wise_label_wise_entity_count[document_title][label] += 1
        
        for k, v in file_wise_label_wise_entity_count.items():
            file_wise_label_wise_entity_count[k] = dict(sorted(v.items()))
                
        self._eda_summary["total_files"] = len(ner_data_items)
        self._eda_summary["total_sentences"] = total_sentences
        self._eda_summary["total_tokens"] = total_tokens
        self._eda_summary["total_labels"] = len(label_wise_entity_count)
        self._eda_summary["total_entities"] = total_entities
        self._eda_summary["file_wise_sentence_token_entity_count"] = file_wise_sentence_token_entity_count
        self._eda_summary["label_wise_entity_count"] = dict(sorted(label_wise_entity_count.items()))
        self._eda_summary["file_wise_label_wise_entity_count"] = dict(sorted(file_wise_label_wise_entity_count.items()))

        rare_labels: List[str] = list()
        if rare_label_entity_count_threshold > 0:
            rare_labels = [label for label, count in label_wise_entity_count.items() if count <= rare_label_entity_count_threshold]
        
        rare_label_wise_entity_items: Dict[str, List[Dict[str, Any]]] = dict()
        for item in self._ner_data_items:
            document_title = item.get("document_title", "")
            entities = item.get("entities", [])
            for entity in entities:
                label = entity.get("label", "")
                if label:
                    if label in rare_labels:
                        entity.update({"document_title": document_title})
                        if label not in rare_label_wise_entity_items:
                            rare_label_wise_entity_items[label] = list()
                        rare_label_wise_entity_items[label].append(entity)
        self._eda_summary["rare_label_wise_entity_items"] = dict(sorted(rare_label_wise_entity_items.items()))

    def get_eda_summary(self) -> Dict[str, Any]:
        """
        Retrieve the exploratory data analysis (EDA) summary of the NER data.
        :return: The EDA summary dictionary.
        """
        if not self._eda_summary:
            self._build_eda_summary()
        return self._eda_summary
    
    def _build_and_save_ner_dataframe(self) -> None:
        """
        Build a pandas DataFrame from the NER data items and exploratory data analysis (EDA) summary.
        :return: None
        """
        ner_data_items = self.get_ner_data_items()
        eda_summary = self.get_eda_summary()
        tuples = list()
        for idx, item in enumerate(ner_data_items):
            document_title = item.get("document_title", "")
            document_text = item.get("document_text", "")
            sentences = json.dumps(item.get("sentences", []), ensure_ascii=False)
            tokens = json.dumps(item.get("tokens", []), ensure_ascii=False)
            entities = json.dumps(item.get("entities", []), ensure_ascii=False)
            sentence_count = eda_summary.get("file_wise_sentence_token_entity_count", {}).get(document_title, (0, 0, 0))[0]
            token_count = eda_summary.get("file_wise_sentence_token_entity_count", {}).get(document_title, (0, 0, 0))[1]
            entity_count = eda_summary.get("file_wise_sentence_token_entity_count", {}).get(document_title, (0, 0, 0))[2]
            label_wise_entity_count = json.dumps(eda_summary.get("file_wise_label_wise_entity_count", {}).get(document_title, {}), ensure_ascii=False)
            bioes_text = self._build_bioes_text_for_ner_data_item(item)

            tuples.append((
                idx, 
                document_title, 
                document_text, 
                sentences, 
                tokens, 
                entities, 
                sentence_count, 
                token_count, 
                entity_count,
                label_wise_entity_count, 
                bioes_text
            ))
            
        self._ner_dataframe = pd.DataFrame(
            tuples,
            columns=[
                "ID", 
                "document_title", 
                "document_text", 
                "sentences", 
                "tokens", 
                "entities", 
                "sentence_count", 
                "token_count", 
                "entity_count", 
                "label_wise_entity_count", 
                "bioes_text"
            ]
        )
        self._ner_dataframe.to_csv(self._get_grascco_ner_data_csv_file_path())
    
    def _get_grascco_ner_data_csv_file_path(self) -> Path:
        """
        Get the file path for the NER data CSV file.
        :return: The Path object representing the CSV file path.
        """
        return self._data_root / "grascco_ner_data.csv"
    
    def get_ner_dataframe(self) -> DataFrame:
        """
        Retrieve the pandas DataFrame built from NER data items.
        :return: The pandas DataFrame.
        """
        grascco_ner_data_csv_file_path = self._get_grascco_ner_data_csv_file_path()
        if grascco_ner_data_csv_file_path.exists():
            self._ner_dataframe = pd.read_csv(grascco_ner_data_csv_file_path, index_col=0)
        else:
            self._build_and_save_ner_dataframe()
        return self._ner_dataframe
    
    def get_train_dev_test_datasetdict(self, k: int = 1) -> DatasetDict:
        
        """
        Retrieve the train, dev, and test dataframes for the specified fold.
        :param k: The fold number to retrieve (1-based index).
        :return: A DatasetDict containing the train, dev, and test datasets.
        """

        random_state: int = 2025
        ner_df = self.get_ner_dataframe()

        label_wise_files: Dict[str, Set[str]] = dict()
        rare_label_wise_entity_items = self.get_eda_summary().get("rare_label_wise_entity_items", {})
        for label, items in rare_label_wise_entity_items.items():
            files = set([item["document_title"] for item in items])
            label_wise_files[label] = files

        # for label, files in label_wise_files.items():
        #     print(f"Label: {label}, Files: {files}, Count: {len(files)}")

        # Label: CONTACT_EMAIL, Files: {'Weil.txt'}, Count: 1
        # Label: CONTACT_FAX, Files: {'Weil.txt', 'Schielaug.txt', 'Joubert.txt', 'Meulengracht.txt', 'Schuh.txt', 'Dupuytren.txt'}, Count: 6
        # Label: LOCATION_COUNTRY, Files: {'Waldenström.txt', 'Recklinghausen.txt'}, Count: 2
        # Label: LOCATION_ORGANIZATION, Files: {'Joubert.txt', 'Theodor.txt'}, Count: 2
        # Label: NAME_EXT, Files: {'Fleischmann.txt'}, Count: 1
        # Label: NAME_RELATIVE, Files: {'Amanda_Alzheimer.txt'}, Count: 1
        # Label: NAME_USERNAME, Files: {'Tupolev_3.txt'}, Count: 1
        # Label: PROFESSION, Files: {'Boeck.txt', 'Theodor.txt'}, Count: 2

        fixed_train_items = [
            'Weil.txt', 
            'Fleischmann.txt', 
            'Amanda_Alzheimer.txt', 
            'Tupolev_3.txt', 
            'Schielaug.txt'
            'Waldenström.txt',
            'Theodor.txt'
        ]
        fixed_test_items = [
            'Joubert.txt',
            'Meulengracht.txt',
            'Recklinghausen.txt',
            'Boeck.txt'
        ]
        fixed_dev_items = [
            'Schuh.txt',
            'Dupuytren.txt'
        ]

        # remove fixed items from ner_df
        remaining_ner_df = ner_df[~ner_df['document_title'].isin(fixed_train_items + fixed_test_items + fixed_dev_items)]
        
        # select 5 more random items from remaining_ner_df for test set and remove them from remaining_ner_df
        remaining_test_items = random.Random(random_state).sample(remaining_ner_df.document_title.tolist(), 5)
        remaining_ner_df = remaining_ner_df[~remaining_ner_df['document_title'].isin(remaining_test_items)]

        test_items = fixed_test_items + remaining_test_items

        remaining_ner_df.reset_index(drop=True, inplace=True)

        fold_tuples = list()
        splits = list(KFold(n_splits=5, shuffle=True, random_state=random_state).split(remaining_ner_df.index.to_numpy()))
        train_dev_k_folds = self.get_train_dev_folds()
        for index, fold in enumerate(train_dev_k_folds):
            train_indices = list()
            fold_train_indices = fold[1]
            for fold_train_index in fold_train_indices:
                train_indices += list(splits[fold_train_index][1])
            dev_indices = list()
            fold_dev_indices = fold[2]
            for fold_dev_index in fold_dev_indices:
                dev_indices += list(splits[fold_dev_index][1])
            fold_tuples.append((
                index + 1,
                remaining_ner_df[remaining_ner_df.index.isin(train_indices)].document_title.tolist() + fixed_train_items,
                remaining_ner_df[remaining_ner_df.index.isin(dev_indices)].document_title.tolist() + fixed_dev_items,
                test_items
            ))
        
        kth_tuple = fold_tuples[k-1]
        train_ds = Dataset.from_pandas(ner_df[ner_df.document_title.isin(kth_tuple[1])])
        dev_ds = Dataset.from_pandas(ner_df[ner_df.document_title.isin(kth_tuple[2])])
        test_ds = Dataset.from_pandas(ner_df[ner_df.document_title.isin(kth_tuple[3])])

        return DatasetDict({
            "train": train_ds,
            "dev": dev_ds,
            "test": test_ds
        })


    @staticmethod
    def get_train_dev_folds(n_fold: int = 5) -> List[Tuple]:
        fold_tuples = list()
        indices = list(range(n_fold))
        for index in indices:
            rolled_indices = np.roll(indices, -index)
            train_indices = list(rolled_indices[0:(n_fold - 1)])
            dev_indices = [rolled_indices[-1]]
            fold_tuples.append((
                index + 1,
                train_indices,
                dev_indices
            ))
        return fold_tuples