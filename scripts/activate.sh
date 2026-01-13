#!/usr/bin/env bash

# ========== User Configuration ==========
# Please set your SSH key path
KEY="$HOME/.ssh/id_rsa"
# KEY="$HOME/.ssh/id_ed25519"
# ========================================

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "ERROR: Please source this script so environment variables persist in your current shell:"
  echo "  . scripts/activate.sh"
  echo "  # or"
  echo "  source scripts/activate.sh"
  exit 1
fi

# Load env.sh to ensure .env is created
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"

if [ -z "${KEY:-}" ]; then
  echo "ERROR: SSH key path is not set. Please set KEY (private key path) in scripts/activate.sh." >&2
  return 1
elif [ ! -f "$KEY" ]; then
  echo "ERROR: SSH private key file not found: $KEY" >&2
  echo "      Please update KEY (private key path) in scripts/activate.sh." >&2
  return 1
fi

if [[ -z "${SSH_AUTH_SOCK:-}" ]] || ! ssh-add -l >/dev/null 2>&1; then
  eval "$(ssh-agent -s)" >/dev/null
fi

ssh-add "$KEY" </dev/null || true
ssh-add -l || true
echo "${SSH_AUTH_SOCK:-}"