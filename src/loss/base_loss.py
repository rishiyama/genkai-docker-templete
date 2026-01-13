import torch
from abc import ABC, abstractmethod

class BaseLoss(torch.nn.Module, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def forward(self, *args, **kwargs):
        pass

    def _create_loss_dict(self, **losses):
        return {key: value.item() if isinstance(value, torch.Tensor) else value for key, value in losses.items()}

