# Training with Docker
## Environment Setup

To set up the environment, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install dependencies:
   ```bash
   uv sync
   uv pip install -e .
   ```

### Optional: Using Docker

Alternatively, you can use Docker to set up the environment:
1. Build the Docker image and Run the container:
   ```bash
   source scripts/env.sh
   docker compose up -d --build
   docker compose exec dev bash
   ```
   - `scripts/env.sh`: sets basic environment variables (UID/GID, .env)

> [!TIP]
>
> **FYI**: Developer mode with SSH access for git operations:
> ```bash
> source scripts/activate.sh
> docker compose -f compose.yaml -f compose.ssh.yaml up -d
> docker compose -f compose.yaml -f compose.ssh.yaml exec dev bash
> ```
> Inside the container, verify SSH access to GitHub:
> ```bash
> ssh -T git@github.com
> ```
> - `scripts/activate.sh`: starts ssh-agent and adds SSH keys for git access


2. Inside the Docker container, install dependencies:
   ```bash
   uv sync
   uv pip install -e .
   ```

## Usage
- Simple VAE training:
```bash
python scripts/train.py --config configs/config.yaml
```