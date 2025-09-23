from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))

from data_handlers.grascco_data_handler import GrasccoDataHandler
from typing import Dict
from utils.project_utils import ProjectUtils
from utils.report_utils import ReportUtils
from utils.plot_utils import PlotUtils

import json

if __name__ == "__main__":
    project_root: Path = ProjectUtils.get_project_root()
    data_handler = GrasccoDataHandler(project_root)
    
    ### Generate EDA summary and save as JSON
    """ 
    eda_summary = data_handler.get_eda_summary()
    with (project_root / "data" / "eda_summary.json").open("w", encoding="utf-8") as f:
        json.dump(eda_summary, f, ensure_ascii=False, indent=4)
    """
    
    ### Get fold wise stats for all labels
    """ 
    label_order = [
        "DATE",
        "NAME_PATIENT",
        "NAME_DOCTOR",
        "NAME_TITLE",
        "LOCATION_CITY",
        "ID",
        "LOCATION_ZIP",
        "LOCATION_HOSPITAL",
        "LOCATION_STREET",
        "AGE",
        "CONTACT_PHONE",
        "CONTACT_FAX",
        "LOCATION_COUNTRY",
        "LOCATION_ORGANIZATION",
        "PROFESSION",
        "CONTACT_EMAIL",
        "NAME_EXT",
        "NAME_RELATIVE",
        "NAME_USERNAME"
    ]
    fold_stats = dict()
    for fold in range(1, 6):
        fold_datasetdict = data_handler.get_train_dev_test_datasetdict(fold)
        fold_stats[fold] = data_handler.get_fold_stats(fold_datasetdict, label_order)
    print(json.dumps(fold_stats, indent=4))
    """

    ### Get model wise, sample size wise and fold wise metrics from classification report text files
    """ 
    model_wise_metrics = ReportUtils.get_model_and_sample_size_and_fold_wise_metrics(project_root / "metrics" / "ner_performance")
    print(json.dumps(model_wise_metrics, indent=4))
    """

    ### Get performance metrics summary by class or statistic
    """
    metrics = ReportUtils.get_performance_metrics_summary_by_class_or_stat(
        metrics_dir=project_root / "metrics" / "ner_performance",
        model_alias_dict={
            "google-bert-base-german-cased": "germanBERT-base",
            "facebookai-xlm-roberta-large": "XLM-RoBERTa-large",
            "deepset-gelectra-large": "gELECTRA-large"
        },
        stat_or_label="PROFESSION",
    )
    print(metrics.to_markdown(index=False))
    """

    ### Plot performance comparison of models for selected classes or statistics
    """
    figure_output_dir: Path = project_root / "reports" / "figures"
    metrics_dir: Path = project_root / "metrics" / "ner_performance"
    model_alias_dict: Dict[str, str] = {
        "google-bert-base-german-cased": "germanBERT-base",
        "facebookai-xlm-roberta-large": "XLM-RoBERTa-large",
        "deepset-gelectra-large": "gELECTRA-large"
    }

    #### Plot micro avg, macro avg and weighted avg performance comparison of models
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat_list=["micro avg", "macro avg", "weighted avg"],
        plot_config={
            "y_lim_list": [(0.76, 1.004), (0.47, 0.85), (0.76, 1.004)],
            "y_ticks_list": [(0.76, 0.921, 0.04), (0.47, 0.73, 0.05), (0.76, 0.921, 0.04)]
        },
        show_logs=True
    )

    #### Plot DATE, NAME_DOCTOR, NAME_PATIENT performance comparison of models
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat_list=["DATE", "NAME_DOCTOR", "NAME_PATIENT"],
        plot_config={
            "y_lim_list": [(0.88, 1.06), (0.60, 1.20), (0.65, 1.175)],
            "y_ticks_list": [(0.88, 1.01, 0.03), (0.60, 1.01, 0.08), (0.65, 1.01, 0.07)]
        },
        show_logs=True
    )

    #### Plot NAME_TITLE, ID, LOCATION_CITY performance comparison of models
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat_list=["NAME_TITLE", "ID", "LOCATION_CITY"],
        plot_config={
            "y_lim_list": [(0.75, 1.125), (0.48, 1.08), (0.40, 1.30)],
            "y_ticks_list": [(0.75, 1.01, 0.05), (0.48, 0.881, 0.08), (0.40, 1.01, 0.10)]
        },
        show_logs=True
    )

    #### Plot LOCATION_STREET, LOCATION_ZIP, CONTACT_PHONE performance comparison of models
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat_list=["LOCATION_STREET", "LOCATION_ZIP", "CONTACT_PHONE"],
        plot_config={
            "y_lim_list": [(0.31, 1.23), (0.20, 1.43), (0.30, 1.37)],
            "y_ticks_list": [(0.31, 0.911, 0.10), (0.20, 1.01, 0.16), (0.30, 1.01, 0.14)]
        },
        show_logs=True
    )

    #### Plot LOCATION_HOSPITAL, CONTACT_FAX, AGE performance comparison of models
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat_list=["LOCATION_HOSPITAL", "CONTACT_FAX", "AGE"],
        plot_config={
            "y_lim_list": [(0.20, 1.20), (0.0, 1.07), (0.55, 1.24)],
            "y_ticks_list": [(0.20, 0.86, 0.13), (0.0, 0.71, 0.14), (0.55, 1.01, 0.09)]
        },
        show_logs=True
    )

    #### Plot LOCATION_COUNTRY, LOCATION_ORGANIZATION, PROFESSION performance comparison of models
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat_list=["LOCATION_COUNTRY", "LOCATION_ORGANIZATION", "PROFESSION"],
        show_logs=True
    )
    """