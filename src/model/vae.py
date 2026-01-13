import torch
import torch.nn as nn
import diffusers


class VAEWrapper(nn.Module):
    def __init__(self, type='AutoencoderKL', model_config=None):
        super(VAEWrapper, self).__init__()
        if type == 'AutoencoderKL':
            self.vae = diffusers.AutoencoderKL.from_pretrained(
                **model_config
            )
        else:
            raise ValueError(f"Unsupported VAE type: {type}")
        
        