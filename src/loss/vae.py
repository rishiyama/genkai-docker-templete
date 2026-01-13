import torch
import torch.nn.functional as F
from loss.base_loss import BaseLoss

class VAELoss(BaseLoss):
    """
    Standard VAE loss:
      total = recon_loss + beta * kl_loss

    recon_loss:
      - "l1": mean absolute error
      - "l2": mean squared error
      - "bce": binary cross entropy (if your data is in [0,1])

    kl_loss:
      - computed from posterior.kl() if available
      - otherwise computed from mean/logvar if provided
    """

    def __init__(
        self,
        recon_type: str = "l1",
        beta: float = 1e-6,
        kl_reduction: str = "mean",      # "mean" or "sum"
        recon_reduction: str = "mean",   # "mean" or "sum"
    ):
        super().__init__()
        recon_type = recon_type.lower()
        if recon_type not in {"l1", "l2", "bce"}:
            raise ValueError(f"Unknown recon_type: {recon_type}")
        if kl_reduction not in {"mean", "sum"}:
            raise ValueError(f"Unknown kl_reduction: {kl_reduction}")
        if recon_reduction not in {"mean", "sum"}:
            raise ValueError(f"Unknown recon_reduction: {recon_reduction}")

        self.recon_type = recon_type
        self.beta = float(beta)
        self.kl_reduction = kl_reduction
        self.recon_reduction = recon_reduction

    def _reduce(self, x: torch.Tensor, reduction: str) -> torch.Tensor:
        return x.mean() if reduction == "mean" else x.sum()

    def _recon_loss(self, recon: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        if self.recon_type == "l1":
            loss = (recon - target).abs()
        elif self.recon_type == "l2":
            loss = (recon - target).pow(2)
        else:  # "bce"
            # expects target in [0,1], recon as logits or probs?
            # Here we assume recon is already in [0,1]. If recon are logits, use BCEWithLogitsLoss.
            loss = F.binary_cross_entropy(recon, target, reduction="none")

        return self._reduce(loss, self.recon_reduction)

    def _kl_loss(self, posterior) -> torch.Tensor:
        # diffusers DiagonalGaussianDistribution usually provides .kl()
        if hasattr(posterior, "kl") and callable(posterior.kl):
            kl = posterior.kl()
            # kl may be shape (N,) or (N, ...) depending on impl; reduce safely:
            if isinstance(kl, torch.Tensor) and kl.ndim > 0:
                kl = kl.mean(dim=list(range(1, kl.ndim)))  # per-sample
            return self._reduce(kl, self.kl_reduction)

        raise ValueError("posterior does not provide .kl(); pass a posterior with .kl()")

    def forward(
        self,
        *,
        recon: torch.Tensor,
        target: torch.Tensor,
        posterior,
    ):
        recon_loss = self._recon_loss(recon, target)
        kl_loss = self._kl_loss(posterior)
        total = recon_loss + self.beta * kl_loss

        return total, self._create_loss_dict(
            total=total,
            recon=recon_loss,
            kl=kl_loss,
            beta=self.beta,
        )
