from pandas import DataFrame
from pathlib import Path
from typing import Any, Dict, List, Union

import numpy as np
import pandas as pd
import re


class ReportUtils:
    """
    Utility class for parsing and preparing report stats based on classification reports text files.
    """

    @staticmethod
    def get_classification_report_dict(report_file_path: Path) -> Dict[str, Dict[str, Any]]:
        """
        Parses a classification report from a text file and returns a dictionary with metrics for each class or statistic.
        :param report_file_path: Path to the classification report text file.
        :return: Dictionary with class or statistic name as keys and their metrics as values.
        """
        
        metrics_dict: Dict[str, Dict[str, Any]] = dict()
        lines: List[str] = list()
        with (report_file_path.open('r', encoding='utf-8')) as file_reader:
            lines = file_reader.readlines()
        start_processing = False
        for line in lines:
            line = line.strip()
            if "precision" in line and "recall" in line and "f1-score" in line and "support" in line:
                start_processing = True
                continue            
            if start_processing:
                match = re.match(r"(\S[\S ]*\S)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+)", line)
                if match:
                    class_name, precision, recall, f1_score, support = match.groups()
                    metrics_dict[class_name] = {
                        "precision": float(precision),
                        "recall": float(recall),
                        "f1-score": float(f1_score),
                        "support": int(support)
                    }
        return metrics_dict
    
    @staticmethod
    def get_model_and_sample_size_and_fold_wise_metrics(metrics_dir: Path) -> Dict[str, Dict[str, Dict[str, Dict]]]:
        """
        Parses classification report text files in a hierarchical dictionary structure.
        :param metrics_dir: Path to the root directory containing classification report text files.
        :return: Nested dictionary with hierarchy in the order of - 
                 (1) model names, 
                 (2) sample sizes, 
                 (3) fold numbers, 
                 (4) class or statistic names and 
                 (5) their metrics (precision, recall, f1-score and support).
        """
        
        model_wise_dict: Dict[str, Dict[str, Dict[str, Dict[str, Dict[str, Any]]]]] = dict()
        metrics_files: List[Path] = list(metrics_dir.glob("**/*.txt"))
        model_names: List[str] = [item.name for item in metrics_dir.iterdir() if item.is_dir()]
        model_wise_files: Dict[str, List[Path]] = {model_name: [path for path in metrics_files if model_name in str(path.resolve())] for model_name in model_names}
        for model_name in model_names:
            sample_size_wise_dict: Dict[str, Dict[str, Dict[str, Dict[str, Any]]]] = dict()
            sample_sizes: List[str] = list(set([path.name.split("-")[0] for path in model_wise_files[model_name]]))
            sample_size_wise_files: Dict[str, List[Path]] = {sample_size: [path for path in model_wise_files[model_name] if sample_size in str(path.resolve())] for sample_size in sample_sizes}
            for sample_size in sample_sizes:
                fold_wise_dict: Dict[str, Dict[str, Dict[str, Any]]] = dict()
                for path in sample_size_wise_files[sample_size]:
                    fold: str = path.name.split("-")[1].split(".")[0]
                    fold_dict: Dict[str, Dict[str, Any]] = ReportUtils.get_classification_report_dict(path)
                    fold_wise_dict[fold] = fold_dict
                sample_size_wise_dict[sample_size] = dict(sorted(fold_wise_dict.items()))
            model_wise_dict[model_name] = sample_size_wise_dict
        return model_wise_dict

    @staticmethod
    def get_performance_metrics_grouped_by_class_or_stat(metrics_dir: Path, 
                                                         model_names: List[str], 
                                                         sample_size: int = 63, 
                                                         folds: List[int] = [1, 2, 3, 4, 5]) -> Dict[str, List[List[List[Union[float, int]]]]]:
        """
        Collect all metrics (prec./rec./f1./support) for all folds, all models in lists for each class or statistic.
        :param metrics_dir: Path to the root directory containing classification report text files.
        :param model_names: List of model names to include in the output.
        :param sample_size: Sample size to filter the output.
        :param folds: List of fold numbers to include in the output.
        :return: Dictionary with class or statistic name as keys and lists of metrics for each model.
        """
        
        performance_metrics_dict: Dict[str, List[List[List[Union[float, int]]]]] = dict()
        model_wise_dict: Dict[str, Dict[str, Dict[str, Dict[str, Dict[str, Any]]]]] = ReportUtils.get_model_and_sample_size_and_fold_wise_metrics(metrics_dir)
        class_or_stat_names: List[str] = list(model_wise_dict[model_names[0]][f'{sample_size}'][f'K{folds[0]}'].keys())
        for class_or_stat in class_or_stat_names:
            model_metrics_list: List[List[List[Union[float, int]]]] = list()
            for model_name in model_names:
                precisions: List[float] = list()
                recalls: List[float] = list()
                f1_scores: List[float] = list()
                supports: List[int] = list()
                for idx, fold in enumerate(folds):
                    precisions.append(round(model_wise_dict[model_name][f'{sample_size}'][f'K{fold}'][class_or_stat]['precision'], 4))
                    recalls.append(round(model_wise_dict[model_name][f'{sample_size}'][f'K{fold}'][class_or_stat]['recall'], 4))
                    f1_scores.append(round(model_wise_dict[model_name][f'{sample_size}'][f'K{fold}'][class_or_stat]['f1-score'], 4))
                    supports.append(model_wise_dict[model_name][f'{sample_size}'][f'K{fold}'][class_or_stat]['support'])
                model_metrics_list.append([precisions, recalls, f1_scores, supports])
            performance_metrics_dict[class_or_stat] = model_metrics_list
        return performance_metrics_dict

    @staticmethod
    def get_performance_metrics_summary_by_class_or_stat(metrics_dir: Path, 
                                                         model_alias_dict: Dict[str, str], 
                                                         stat_or_label: str) -> DataFrame:
        """
        Prepare a summary table of performance metrics (mean ± std) for a specific class or statistic.
        :param metrics_dir: Path to the root directory containing classification report text files.
        :param model_alias_dict: Dictionary mapping model names to their aliases for display.
        :param stat_or_label: The class name or statistic (e.g., 'micro avg', 'DATE', etc.) to summarize.
        :return: Pandas DataFrame containing the summary table.
        """

        model_names = list(model_alias_dict.keys())
        metrics_data = ReportUtils.get_performance_metrics_grouped_by_class_or_stat(metrics_dir, model_names)
        label_data = np.array(metrics_data[stat_or_label])
        means = np.mean(label_data, axis=2)
        std_devs = np.std(label_data, axis=2)
        table_tuples: List[str] = list()
        for idx in range(len(model_names)):
            precision_str = f'{round(means[idx][0], 2): .2f} ± {round(std_devs[idx][0], 3)}'
            recall_str = f'{round(means[idx][1], 2): .2f} ± {round(std_devs[idx][1], 3)}'
            f1_score_str = f'{round(means[idx][2], 2): .2f} ± {round(std_devs[idx][2], 3)}'
            support_str = f'{int(means[idx][3])} ± {int(std_devs[idx][3])}'
            table_tuples.append((model_alias_dict[model_names[idx]], precision_str, recall_str, f1_score_str, support_str))
        return pd.DataFrame(table_tuples, columns=["Model", "Precision", "Recall", "F1-score", "Support"])