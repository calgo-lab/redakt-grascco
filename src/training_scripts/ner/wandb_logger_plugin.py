from flair.trainers.plugins import TrainerPlugin, MetricRecord
from typing import Any, Dict, Set

import wandb


class WandbLoggerPlugin(TrainerPlugin):
    """
    A TrainerPlugin that logs training metrics to Weights & Biases (wandb).
    """
    def __init__(self, 
                 project: str = "flair-trainer-finetune", 
                 config: Dict[str, Any] = None, 
                 tracked: Set[str] = None, 
                 reinit: bool = True):

        self.project = project
        self.config = dict(config or {})
        self.tracked = set(tracked) if tracked is not None else None
        self.reinit = reinit
        self._run = None
        self._pluggable = None

    def after_setup(self, trainer, **kw):
        self._run = wandb.init(
            project=self.project, 
            config=self.config, 
            reinit=self.reinit
        )

    def metric_recorded(self, record: MetricRecord):
        name = record.joined_name
        if (self.tracked is None) or (name in self.tracked):
            # convert values into wandb-friendly scalars
            value = record.value
            if hasattr(value, "__len__") and not isinstance(value, str):
                value = {f"{name}_{i}": float(v) for i, v in enumerate(value)}
                wandb.log(value, step=record.global_step)
            else:
                wandb.log({name: float(value)}, step=record.global_step)

    def after_model_saved(self, trainer, model, **kw):
        # mark the point when best model is saved
        wandb.log({"best_model_saved": 1}, step=trainer.epoch)

    def after_training(self, trainer, **kw):
        if self._run:
            self._run.finish()
            self._run = None