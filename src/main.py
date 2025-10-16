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
    print(json.dumps(fold_stats, indent=4, ensure_ascii=False))

    printable_fold_stats = dict()
    for fold, stats in fold_stats.items():
        printable_fold_stats[fold] = dict()
        for stat, value in stats.items():
            if stat == "total_files":
                printable_fold_stats[fold]["Total Files"] = (
                    f"Train: {value['train']}<br>"
                    f"Dev: {value['dev']}<br>"
                    f"Test: {value['test']}"
                )
            elif stat == "total_sentences":
                printable_fold_stats[fold]["Total Sentences"] = (
                    f"Train: {value['train']}<br>"
                    f"Dev: {value['dev']}<br>"
                    f"Test: {value['test']}"
                )
            elif stat == "total_tokens":
                printable_fold_stats[fold]["Total Tokens"] = (
                    f"Train: {value['train']}<br>"
                    f"Dev: {value['dev']}<br>"
                    f"Test: {value['test']}"
                )
            elif stat == "total_entities":
                printable_fold_stats[fold]["Total Entities"] = (
                    f"Train: {value['train']}<br>"
                    f"Dev: {value['dev']}<br>"
                    f"Test: {value['test']}"
                )
            elif stat == "train_files":
                printable_fold_stats[fold]["Train Files"] = "<br>".join(value)
            elif stat == "dev_files":
                printable_fold_stats[fold]["Dev Files"] = "<br>".join(value)
            elif stat == "test_files":
                printable_fold_stats[fold]["Test Files"] = "<br>".join(value)

            for label in label_order:
                if stat == label:
                    printable_fold_stats[fold][label] = (
                        f"Train: {value['train']}<br>"
                        f"Dev: {value['dev']}<br>"
                        f"Test: {value['test']}"
                    )
    print(json.dumps(printable_fold_stats, indent=4, ensure_ascii=False))
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
        model_alias_dict = {
            "google-bert--bert-base-german-cased-flert": "bert-base-german-cased",
            "calgo-lab--codealltag-ner-bert-base-german-cased-flert-175k": "codealltag-bert-base-german-cased",
            "xlm-roberta-large-flert": "xlm-roberta-large",
            "calgo-lab--codealltag-ner-xlm-roberta-large-flert-175k": "codealltag-xlm-roberta-large",
            "deepset--gelectra-large-flert": "gelectra-large",
            "calgo-lab--codealltag-ner-gelectra-large-flert-175k": "codealltag-gelectra-large"
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
        "google-bert--bert-base-german-cased-flert": "bert-base-german-cased",
        "xlm-roberta-large-flert": "xlm-roberta-large",
        "deepset--gelectra-large-flert": "gelectra-large"
    }
    
    #### Plot micro avg, macro avg and weighted avg performance comparison of models
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_classes_or_stats(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat_list=["micro avg", "macro avg", "weighted avg"],
        plot_config={
            "y_lim_list": [(0.78, 1.004), (0.49, 0.79), (0.78, 1.004)],
            "y_ticks_list": [(0.78, 0.931, 0.03), (0.49, 0.691, 0.04), (0.78, 0.931, 0.03)]
        },
        show_logs=True
    )
    
    #### Plot DATE, NAME_DOCTOR, NAME_PATIENT performance comparison of models
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_classes_or_stats(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat_list=["DATE", "NAME_DOCTOR", "NAME_PATIENT"],
        plot_config={
            "y_lim_list": [(0.88, 1.053), (0.60, 1.178), (0.55, 1.20)],
            "y_ticks_list": [(0.88, 1.01, 0.03), (0.60, 1.01, 0.08), (0.55, 1.01, 0.09)]
        },
        show_logs=True
    )
    
    #### Plot NAME_TITLE, ID, LOCATION_CITY performance comparison of models
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_classes_or_stats(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat_list=["NAME_TITLE", "ID", "LOCATION_CITY"],
        plot_config={
            "y_lim_list": [(0.69, 1.125), (0.59, 1.095), (0.44, 1.247)],
            "y_ticks_list": [(0.69, 0.991, 0.06), (0.59, 0.941, 0.07), (0.44, 1.01, 0.14)]
        },
        show_logs=True
    )

    #### Plot LOCATION_STREET, LOCATION_ZIP, CONTACT_PHONE performance comparison of models
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_classes_or_stats(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat_list=["LOCATION_STREET", "LOCATION_ZIP", "CONTACT_PHONE"],
        plot_config={
            "y_lim_list": [(0.35, 1.285), (0.64, 1.16), (0.05, 1.205)],
            "y_ticks_list": [(0.35, 1.01, 0.13), (0.64, 1.01, 0.06), (0.05, 0.851, 0.20)]
        },
        show_logs=True
    )

    #### Plot LOCATION_HOSPITAL, CONTACT_FAX, AGE performance comparison of models
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_classes_or_stats(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat_list=["LOCATION_HOSPITAL", "CONTACT_FAX", "AGE"],
        plot_config={
            "y_lim_list": [(0.20, 1.235), (0.0, 0.87), (0.45, 1.245)],
            "y_ticks_list": [(0.20, 0.921, 0.12), (0.0, 0.61, 0.12), (0.45, 1.01, 0.11)]
        },
        show_logs=True
    )
    
    #### Plot LOCATION_COUNTRY, LOCATION_ORGANIZATION, PROFESSION performance comparison of models
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_classes_or_stats(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat_list=["LOCATION_COUNTRY", "LOCATION_ORGANIZATION", "PROFESSION"],
        show_logs=True
    )
    """

    ### Plot performance comparison of models for selected class or statistic
    """
    figure_output_dir: Path = project_root / "reports" / "figures"
    metrics_dir: Path = project_root / "metrics" / "ner_performance"
    model_alias_dict: Dict[str, str] = {
        "google-bert--bert-base-german-cased-flert": "bert-base-german-cased",
        "calgo-lab--codealltag-ner-bert-base-german-cased-flert-175k": "codealltag-bert-base-german-cased",
        "xlm-roberta-large-flert": "xlm-roberta-large",
        "calgo-lab--codealltag-ner-xlm-roberta-large-flert-175k": "codealltag-xlm-roberta-large",
        "deepset--gelectra-large-flert": "gelectra-large",
        "calgo-lab--codealltag-ner-gelectra-large-flert-175k": "codealltag-gelectra-large"
    }

    #### Plot micro avg performance comparison of models
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="micro avg",
        plot_in_pairs=True,
        plot_config={
            "y_lim": (0.78, 1.08),
            "y_ticks": (0.78, 0.931, 0.03)
        },
        show_logs=True
    )

    #### Plot macro avg performance comparison of models
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="macro avg",
        plot_in_pairs=True,
        plot_config={
            "y_lim": (0.48, 0.96),
            "y_ticks": (0.48, 0.721, 0.06)
        },
        show_logs=True
    )
    
    #### Plot weighted avg performance comparison of models
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="weighted avg",
        plot_in_pairs=True,
        plot_config={
            "y_lim": (0.78, 1.08),
            "y_ticks": (0.78, 0.931, 0.03)
        },
        show_logs=True
    )
    
    #### Plot performance comparison of models for label DATE
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="DATE",
        plot_in_pairs=True,
        plot_config={
            "y_lim": (0.88, 1.12),
            "y_ticks": (0.88, 1.01, 0.03)
        },
        show_logs=True
    )
    
    #### Plot performance comparison of models for label NAME_DOCTOR
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="NAME_DOCTOR",
        plot_in_pairs=True,
        plot_config={
            "y_lim": (0.60, 1.40),
            "y_ticks": (0.60, 1.01, 0.08)
        },
        show_logs=True
    )
    
    #### Plot performance comparison of models for label NAME_PATIENT
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="NAME_PATIENT",
        plot_in_pairs=True,
        plot_config={
            "y_lim": (0.55, 1.45),
            "y_ticks": (0.55, 1.01, 0.09)
        },
        show_logs=True
    )

    #### Plot performance comparison of models for label NAME_TITLE
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="NAME_TITLE",
        plot_in_pairs=True,
        plot_config={
            "y_lim": (0.68, 1.32),
            "y_ticks": (0.68, 1.01, 0.08)
        },
        show_logs=True
    )

    #### Plot performance comparison of models for label ID
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="ID",
        plot_in_pairs=True,
        plot_config={
            "y_lim": (0.52, 1.48),
            "y_ticks": (0.52, 1.01, 0.12)
        },
        show_logs=True
    )
    
    #### Plot performance comparison of models for label LOCATION_CITY
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="LOCATION_CITY",
        plot_in_pairs=True,
        plot_config={
            "y_lim": (0.44, 1.56),
            "y_ticks": (0.44, 1.01, 0.14)
        },
        show_logs=True
    )
    
    #### Plot performance comparison of models for label LOCATION_STREET
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="LOCATION_STREET",
        plot_in_pairs=True,
        plot_config={
            "y_lim": (0.35, 1.65),
            "y_ticks": (0.35, 1.01, 0.13)
        },
        show_logs=True
    )
    
    #### Plot performance comparison of models for label LOCATION_ZIP
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="LOCATION_ZIP",
        plot_in_pairs=True,
        plot_config={
            "y_lim": (0.32, 1.68),
            "y_ticks": (0.32, 1.01, 0.17)
        },
        show_logs=True
    )
    
    #### Plot performance comparison of models for label CONTACT_PHONE
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="CONTACT_PHONE",
        plot_in_pairs=True,
        plot_config={
            "y_lim": (0.05, 1.84),
            "y_ticks": (0.05, 0.951, 0.15)
        },
        show_logs=True
    )

    #### Plot performance comparison of models for label LOCATION_HOSPITAL
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="LOCATION_HOSPITAL",
        plot_in_pairs=True,
        plot_config={
            "y_lim": (0.15, 1.71),
            "y_ticks": (0.15, 0.931, 0.13)
        },
        show_logs=True
    )

    #### Plot performance comparison of models for label CONTACT_FAX
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="CONTACT_FAX",
        plot_in_pairs=True,
        plot_config={
            "y_lim": (0.00, 1.30),
            "y_ticks": (0.00, 0.651, 0.13)
        },
        show_logs=True
    )

    #### Plot performance comparison of models for label AGE
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="AGE",
        plot_in_pairs=True,
        plot_config={
            "y_lim": (0.45, 1.55),
            "y_ticks": (0.45, 1.01, 0.11)
        },
        show_logs=True
    )

    #### Plot performance comparison of models for label LOCATION_COUNTRY
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="LOCATION_COUNTRY",
        plot_in_pairs=True,
        show_logs=True
    )

    #### Plot performance comparison of models for label LOCATION_ORGANIZATION
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="LOCATION_ORGANIZATION",
        plot_in_pairs=True,
        show_logs=True
    )
    
    #### Plot performance comparison of models for label PROFESSION
    PlotUtils.plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(
        figure_output_dir=figure_output_dir,
        metrics_dir=metrics_dir,
        model_alias_dict=model_alias_dict,
        class_or_stat="PROFESSION",
        plot_in_pairs=True,
        show_logs=True
    )
    """