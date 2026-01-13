#!/usr/bin/env bash


# Guard: this script must be sourced (". scripts/setup.sh" or "source scripts/setup.sh")
# If executed as "bash scripts/setup.sh", the exported env vars (e.g., SSH_AUTH_SOCK) won't persist.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "ERROR: Please source this script so environment variables persist in your current shell:"
  echo "  . scripts/env.sh"
  echo "  # or"
  echo "  source scripts/env.sh"
  exit 1
fi


# UID/GID
printf "UID=%s\nGID=%s\n" "$(id -u)" "$(id -g)" > .env
cat .env

