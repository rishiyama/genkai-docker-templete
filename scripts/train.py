import argparse
import os
import json
from datetime import datetime
import shutil

import torch
from torch.utils.data import DataLoader
from omegaconf import OmegaConf
from tqdm.auto import tqdm

import diffusers
from loss.vae import VAELoss
from data.dataset import Random64Dataset

def train_one_epoch(model, dataloader, loss_fn, optimizer, device):
    model.train()
    # total_loss = 0.0
    train_loss_dict = None
    for batch in tqdm(dataloader, desc="Training", leave=False):
        inputs = batch
        inputs = inputs.to(device)

        optimizer.zero_grad()

        enc = model.encode(inputs)
        posterior = enc.latent_dist
        z = posterior.sample()
        outputs = model.decode(z).sample
        loss, loss_dict = loss_fn(recon=outputs, target=inputs, posterior=posterior)
        
        loss.backward()
        optimizer.step()

        if train_loss_dict is None:
            train_loss_dict = {key: 0.0 for key in loss_dict.keys()}
    
        for key, value in loss_dict.items():
            train_loss_dict[key] += value  
        
    
    train_loss_dict = {key: value / len(dataloader) for key, value in train_loss_dict.items()}
    return train_loss_dict

def validate_one_epoch(model, dataloader, loss_fn, device):
    model.eval()
    val_loss_dict = None

    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Validation", leave=False):
            inputs = batch
            inputs = inputs.to(device)

            enc = model.encode(inputs)
            posterior = enc.latent_dist
            z = posterior.sample()
            outputs = model.decode(z).sample


            loss, loss_dict = loss_fn(recon=outputs, target=inputs, posterior=posterior)
            
            if val_loss_dict is None:
                val_loss_dict = {key: 0.0 for key in loss_dict.keys()}
            for key, value in loss_dict.items():
                val_loss_dict[key] += value

    val_loss_dict =  {key: value / len(dataloader) for key, value in val_loss_dict.items()}
    return val_loss_dict


def run(cfg, model, loss_fn, train_dataset, val_dataset, optimizer):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    best_val_loss = float("inf")

    train_loader = DataLoader(train_dataset, batch_size=cfg.train_batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=cfg.val_batch_size, shuffle=False)

    log_file_path = os.path.join(cfg.path.save_dir, "log.jsonl")
    for epoch in tqdm(range(cfg.num_epochs), desc="Epochs"):
        train_loss_dict = train_one_epoch(model, train_loader, loss_fn, optimizer, device)
        val_loss_dict = validate_one_epoch(model, val_loader, loss_fn, device)

        log_entry = {
            "epoch": epoch + 1,
            "train_total_loss": train_loss_dict["total"],
            "val_total_loss": val_loss_dict["total"],
            "train_loss": train_loss_dict,
            "val_loss": val_loss_dict,
        }         

        with open(log_file_path, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")

        if val_loss_dict["total"] < best_val_loss:
            best_val_loss = val_loss_dict["total"]
            model_save_path = os.path.join(cfg.path.save_dir, "best_model.pth")
            torch.save(model.state_dict(), model_save_path)
            print(f"Saved best model with val loss {best_val_loss:.4f} at epoch {epoch + 1}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a model.")
    parser.add_argument("--config", type=str, default="./configs/config.yaml",
                        help="Path to the configuration file (default: ./configs/config.yaml)")
    args = parser.parse_args()

    cfg = OmegaConf.load(args.config)
    cfg.config_path = args.config
    cfg.path.save_dir = os.path.join(
        cfg.path.save_dir, datetime.now().strftime("%Y%m%d-%H%M%S"))
    os.makedirs(cfg.path.save_dir, exist_ok=True)

    OmegaConf.save(cfg, os.path.join(cfg.path.save_dir, "config.yaml"))
    shutil.copy(os.path.realpath(__file__), os.path.join(cfg.path.save_dir, os.path.basename(__file__)))

    # Placeholder for model, loss function, and datasets
    model_config = dict(cfg.model.vae[cfg.model.vae.type])

    model = diffusers.AutoencoderKL(**model_config)
    loss_fn = VAELoss(
        recon_type=cfg.loss.vae.recon_type,
        beta=cfg.loss.vae.beta,
        kl_reduction=cfg.loss.vae.kl_reduction,
        recon_reduction=cfg.loss.vae.recon_reduction,
    )

    dataset = Random64Dataset(n=1024, channels=cfg.data.channels, size=cfg.data.image_size)
    train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(
        dataset,
        [cfg.train_val_test_ratio[0], cfg.train_val_test_ratio[1], cfg.train_val_test_ratio[2]],
        generator=torch.Generator().manual_seed(cfg.seed)
    )

    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg.learning_rate)

    run(cfg, model, loss_fn, train_dataset, val_dataset, optimizer)
