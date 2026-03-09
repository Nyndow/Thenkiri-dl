#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
REQ_FILE="$ROOT_DIR/requirements.txt"

log() {
  printf '\n[install] %s\n' "$1"
}

have_cmd() {
  command -v "$1" >/dev/null 2>&1
}

require_file() {
  if [[ ! -f "$1" ]]; then
    echo "Missing required file: $1"
    exit 1
  fi
}

install_system_deps() {
  if [[ "${SKIP_SYSTEM_DEPS:-0}" == "1" ]]; then
    log "Skipping system package installation (SKIP_SYSTEM_DEPS=1)."
    return
  fi

  if have_cmd apt-get; then
    log "Installing system dependencies with apt-get..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-venv python3-pip wget aria2
  elif have_cmd dnf; then
    log "Installing system dependencies with dnf..."
    sudo dnf install -y python3 python3-virtualenv python3-pip wget aria2
  elif have_cmd pacman; then
    log "Installing system dependencies with pacman..."
    sudo pacman -Sy --noconfirm python python-pip python-virtualenv wget aria2
  elif have_cmd zypper; then
    log "Installing system dependencies with zypper..."
    sudo zypper --non-interactive install python3 python3-pip python3-virtualenv wget aria2
  else
    log "No supported package manager detected. Install these manually: python3, python3-venv, pip, wget, aria2"
  fi
}

setup_python_env() {
  log "Setting up Python virtual environment..."

  if ! have_cmd python3; then
    echo "python3 is not installed or not in PATH."
    exit 1
  fi

  require_file "$REQ_FILE"

  python3 -m venv "$VENV_DIR"
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate"

  python -m pip install --upgrade pip
  python -m pip install -r "$REQ_FILE"

  deactivate
}

write_env_file() {
  local env_file="$ROOT_DIR/.env"
  if [[ -f "$env_file" ]]; then
    log ".env already exists. Leaving it unchanged."
    return
  fi

  log "Creating default .env file..."
  cat > "$env_file" <<EOT
DOWNLOAD_PATH=./downloads
EOT
}

print_next_steps() {
  cat <<EOT

Installation complete.

Next steps:
  source .venv/bin/activate
  python main.py

Optional:
  Set DOWNLOAD_PATH in .env to your preferred folder.
EOT
}

main() {
  cd "$ROOT_DIR"
  install_system_deps
  setup_python_env
  write_env_file
  print_next_steps
}

main "$@"
