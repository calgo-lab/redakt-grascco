from matplotlib.ticker import FormatStrFormatter
from pathlib import Path
from typing import Any, Dict, List, Union
from utils.report_utils import ReportUtils

import matplotlib.pyplot as plt
import numpy as np

class PlotUtils:
    """
    Utility class for plotting figures and charts.
    """

    @staticmethod
    def plot_entity_prediction_performance_comparison_of_models_for_class_or_stat(figure_output_dir: Path, 
                                                                                  metrics_dir: Path, 
                                                                                  model_alias_dict: Dict[str, str], 
                                                                                  class_or_stat_list: List[str], 
                                                                                  metrics: List[str] = ['Prec', 'Rec', 'F1'], 
                                                                                  plot_config: Dict[str, Any] = {
                                                                                      "n_rows": 1, 
                                                                                      "n_cols": 3, 
                                                                                      "figsize": (15, 4), 
                                                                                      "subplots_wspace": 0.50, 
                                                                                      "bar_width": 0.004, 
                                                                                      "space_between_metric_bars": 0.02, 
                                                                                      "bar_colors": ['skyblue', 'yellowgreen', 'rosybrown'], 
                                                                                      "edge_colors": ['dodgerblue', 'darkgreen', 'brown'], 
                                                                                      "error_kw_dict": {
                                                                                          'capsize': 4, 
                                                                                          'elinewidth': 1.5, 
                                                                                          'capthick': 1.5
                                                                                      },
                                                                                      "title_fontsize": 17, 
                                                                                      "y_lim_list": [(0.00, 1.52), (0.00, 1.52), (0.00, 1.52)], 
                                                                                      "y_ticks_list": [(0.00, 1.01, 0.20), (0.00, 1.01, 0.20), (0.00, 1.01, 0.20)], 
                                                                                      "y_ticks_labelsize": 15, 
                                                                                      "y_label_spec": ('Scores', 15, 5), 
                                                                                      "y_grid_spec": ('--', 0.7), 
                                                                                      "x_ticks_labelsize": 15, 
                                                                                      "legend_spec": ('upper right', 12),
                                                                                  }, 
                                                                                  figure_file_ext: str = "jpg", 
                                                                                  figure_name: Union[str, None] = None, 
                                                                                  figure_name_prefix: Union[str, None] = "entity_prediction_performance_comparison_of_models_", 
                                                                                  figure_dpi: int = 600, 
                                                                                  show_logs: bool = False) -> None:
        """
        Utility method to plot entity prediction performance comparison of models for specified classes or statistics.
        The method reads performance metrics from the specified directory, processes the data, and generates bar plots
        comparing the performance of different models for each specified class or statistic.
        :param figure_output_dir: Directory to save the generated figure.
        :param metrics_dir: Directory containing the performance metrics files.
        :param model_alias_dict: Dictionary mapping model identifiers to their display names.
        :param class_or_stat_list: List of classes or statistics to plot.
        :param metrics: List of performance metrics to consider (default: ['Prec', 'Rec', 'F1']).
        :param plot_config: Configuration dictionary for plot aesthetics and layout.
        :param figure_file_ext: File extension for the saved figure (default: 'jpg').
        :param figure_name: Name of the figure file (without extension). If None, a name will be generated.
        :param figure_name_prefix: Prefix for the figure name if figure_name is None (default: 'entity_prediction_performance_comparison_of_models_').
        :param figure_dpi: DPI for the saved figure (default: 600).
        :param show_logs: Whether to print logs during processing (default: False).
        :return: None
        """

        if "n_rows" not in plot_config or plot_config["n_rows"] is None:
            plot_config["n_rows"] = 1
        if "n_cols" not in plot_config or plot_config["n_cols"] is None:
            plot_config["n_cols"] = len(class_or_stat_list)
        if "figsize" not in plot_config or plot_config["figsize"] is None:
            plot_config["figsize"] = (15, 4)
        if "subplots_wspace" not in plot_config or plot_config["subplots_wspace"] is None:
            plot_config["subplots_wspace"] = 0.50
        if "bar_width" not in plot_config or plot_config["bar_width"] is None:
            plot_config["bar_width"] = 0.004
        if "space_between_metric_bars" not in plot_config or plot_config["space_between_metric_bars"] is None:
            plot_config["space_between_metric_bars"] = 0.02
        if "bar_colors" not in plot_config or plot_config["bar_colors"] is None:
            plot_config["bar_colors"] = ['skyblue', 'yellowgreen', 'rosybrown']
        if "edge_colors" not in plot_config or plot_config["edge_colors"] is None:
            plot_config["edge_colors"] = ['dodgerblue', 'darkgreen', 'brown']
        if "error_kw_dict" not in plot_config or plot_config["error_kw_dict"] is None:
            plot_config["error_kw_dict"] = {
                'capsize': 4, 
                'elinewidth': 1.5, 
                'capthick': 1.5
            }
        if "title_fontsize" not in plot_config or plot_config["title_fontsize"] is None:
            plot_config["title_fontsize"] = 17
        if "y_lim_list" not in plot_config or plot_config["y_lim_list"] is None:
            plot_config["y_lim_list"] = [(0.00, 1.52) for _ in class_or_stat_list]
        if "y_ticks_list" not in plot_config or plot_config["y_ticks_list"] is None:
            plot_config["y_ticks_list"] = [(0.00, 1.01, 0.20) for _ in class_or_stat_list]
        if "y_ticks_labelsize" not in plot_config or plot_config["y_ticks_labelsize"] is None:
            plot_config["y_ticks_labelsize"] = 15
        if "y_label_spec" not in plot_config or plot_config["y_label_spec"] is None:
            plot_config["y_label_spec"] = ('Scores', 15, 5)
        if "y_grid_spec" not in plot_config or plot_config["y_grid_spec"] is None:
            plot_config["y_grid_spec"] = ('--', 0.7)
        if "x_ticks_labelsize" not in plot_config or plot_config["x_ticks_labelsize"] is None:
            plot_config["x_ticks_labelsize"] = 15
        if "legend_spec" not in plot_config or plot_config["legend_spec"] is None:
            plot_config["legend_spec"] = ('upper right', 12)
        
        metrics_data = ReportUtils.get_performance_metrics_grouped_by_class_or_stat(
            metrics_dir,
            list(model_alias_dict.keys())
        )

        fig, axes = plt.subplots(
            nrows=plot_config["n_rows"], 
            ncols=plot_config["n_cols"], 
            figsize=plot_config["figsize"]
        )
        fig.subplots_adjust(wspace=plot_config["subplots_wspace"])
        bar_width = plot_config["bar_width"]
        metrics_plot_idx = np.arange(len(metrics)) * plot_config["space_between_metric_bars"]

        for class_or_stat_idx, class_or_stat in enumerate(class_or_stat_list):

            metrics_data[class_or_stat] = [model_data[:3] for model_data in metrics_data[class_or_stat]]

            class_or_stat_data = np.array(metrics_data[class_or_stat])
            class_or_stat_means = np.mean(class_or_stat_data, axis=2)
            class_or_stat_std_devs = np.std(class_or_stat_data, axis=2)

            if show_logs:
                class_or_stat_min = np.min(class_or_stat_means - class_or_stat_std_devs)
                class_or_stat_max = np.max(class_or_stat_means + class_or_stat_std_devs)
                print(f'{class_or_stat}: [{class_or_stat_min}, {class_or_stat_max}]')

            class_or_stat_upper = np.clip(class_or_stat_means + class_or_stat_std_devs, None, 1.0)
            class_or_stat_lower = np.clip(class_or_stat_means - class_or_stat_std_devs, 0.0, None)
            yerr_class_or_stat = np.array(
                [class_or_stat_means - class_or_stat_lower, 
                 class_or_stat_upper - class_or_stat_means]
            )

            for model_idx, model in enumerate(list(model_alias_dict.values())):
                error_kw_dict = plot_config["error_kw_dict"].copy()
                error_kw_dict.update({'ecolor': plot_config["edge_colors"][model_idx]})
                
                axes[class_or_stat_idx].bar(
                    metrics_plot_idx + (model_idx * bar_width), 
                    class_or_stat_means[model_idx], 
                    bar_width, 
                    label=model, 
                    color=plot_config["bar_colors"][model_idx], 
                    edgecolor=plot_config["edge_colors"][model_idx], 
                    align='center', 
                    yerr=yerr_class_or_stat[:, model_idx], 
                    error_kw=error_kw_dict
                )
            
            axes[class_or_stat_idx].set_title(
                class_or_stat, 
                fontsize=plot_config["title_fontsize"]
            )
            
            axes[class_or_stat_idx].set_ylim(
                plot_config["y_lim_list"][class_or_stat_idx][0], 
                plot_config["y_lim_list"][class_or_stat_idx][1]
            )
            axes[class_or_stat_idx].set_yticks(
                np.arange(
                    plot_config['y_ticks_list'][class_or_stat_idx][0], 
                    plot_config['y_ticks_list'][class_or_stat_idx][1], 
                    plot_config['y_ticks_list'][class_or_stat_idx][2]
                )
            )
            axes[class_or_stat_idx].tick_params(
                axis='y', 
                labelsize=plot_config["y_ticks_labelsize"]
            )
            axes[class_or_stat_idx].set_ylabel(
                plot_config["y_label_spec"][0],
                fontsize=plot_config["y_label_spec"][1],
                labelpad=plot_config["y_label_spec"][2]
            )
            axes[class_or_stat_idx].grid(
                axis='y', 
                linestyle=plot_config["y_grid_spec"][0], 
                alpha=plot_config["y_grid_spec"][1]
            )
            axes[class_or_stat_idx].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            
            axes[class_or_stat_idx].set_xticks(metrics_plot_idx + bar_width)
            axes[class_or_stat_idx].set_xticklabels(metrics)
            axes[class_or_stat_idx].tick_params(
                axis='x', 
                labelsize=plot_config["x_ticks_labelsize"]
            )

            axes[class_or_stat_idx].legend(
                loc=plot_config["legend_spec"][0], 
                fontsize=plot_config["legend_spec"][1]
            )

        figure_output_dir.mkdir(parents=True, exist_ok=True)
        if figure_name is None:
            figure_name = f"{figure_name_prefix}{'_'.join([class_or_stat.lower().replace(' ', '_') for class_or_stat in class_or_stat_list])}"
        plot_file_name = f"{figure_name}.{figure_file_ext}"
        plot_file_path = figure_output_dir / plot_file_name
        plt.savefig(
            plot_file_path, 
            format=figure_file_ext, 
            dpi=figure_dpi, 
            bbox_inches='tight'
        )