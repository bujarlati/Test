#!/usr/bin/env bash
set -euo pipefail

DEFAULT_TARGET="/opt/idle-game"
DEFAULT_SERVICE="idle-game"

usage() {
  cat <<'EOF'
Usage:
  sudo scripts/deploy_package.sh PACKAGE_PATH [TARGET_DIR] [SERVICE_NAME]

Examples:
  sudo /opt/idle-game/scripts/deploy_package.sh /tmp/idle_forest_release.tar.gz
  sudo /opt/idle-game/scripts/deploy_package.sh /tmp/idle_forest_release.zip /opt/idle-game idle-game

The deploy keeps TARGET_DIR/data intact and replaces the rest of the app with
the package contents.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

PACKAGE_PATH="${1:-}"
TARGET="${2:-$DEFAULT_TARGET}"
SERVICE="${3:-${IDLE_GAME_SERVICE:-$DEFAULT_SERVICE}}"

if [[ -z "$PACKAGE_PATH" ]]; then
  usage >&2
  exit 2
fi

if [[ ! -f "$PACKAGE_PATH" ]]; then
  echo "Package not found: $PACKAGE_PATH" >&2
  exit 2
fi

if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
  exec sudo -E bash "$0" "$@"
fi

need_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing command: $1" >&2
    echo "Install it first, for example: sudo apt install -y $2" >&2
    exit 2
  fi
}

need_command rsync rsync

case "$PACKAGE_PATH" in
  *.tar.gz|*.tgz)
    need_command tar tar
    ;;
  *.zip)
    need_command unzip unzip
    ;;
  *)
    echo "Unsupported package type: $PACKAGE_PATH" >&2
    echo "Use .tar.gz, .tgz, or .zip" >&2
    exit 2
    ;;
esac

TMP_DIR="$(mktemp -d)"
RELEASE_DIR="$TMP_DIR/release"
mkdir -p "$RELEASE_DIR"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

case "$PACKAGE_PATH" in
  *.tar.gz|*.tgz)
    tar -xzf "$PACKAGE_PATH" -C "$RELEASE_DIR"
    ;;
  *.zip)
    unzip -q "$PACKAGE_PATH" -d "$RELEASE_DIR"
    ;;
esac

SOURCE="$RELEASE_DIR"
if [[ ! -f "$SOURCE/server.py" ]]; then
  MATCHED_SERVER="$(find "$RELEASE_DIR" -mindepth 2 -maxdepth 2 -name server.py -print -quit)"
  if [[ -n "$MATCHED_SERVER" ]]; then
    SOURCE="$(dirname "$MATCHED_SERVER")"
  fi
fi

if [[ ! -f "$SOURCE/server.py" || ! -f "$SOURCE/web/index.html" ]]; then
  echo "Package does not look like an Idle Forest release." >&2
  echo "Expected server.py and web/index.html in the archive root." >&2
  exit 2
fi

mkdir -p "$TARGET/data"

if systemctl list-unit-files "${SERVICE}.service" >/dev/null 2>&1; then
  echo "Stopping ${SERVICE}..."
  systemctl stop "$SERVICE"
else
  echo "Service ${SERVICE}.service was not found; deploying files only."
fi

echo "Deploying $PACKAGE_PATH to $TARGET ..."
rsync -a --delete --exclude '/data/' "$SOURCE/" "$TARGET/"
mkdir -p "$TARGET/data"

if systemctl list-unit-files "${SERVICE}.service" >/dev/null 2>&1; then
  echo "Starting ${SERVICE}..."
  systemctl start "$SERVICE"
  systemctl status "$SERVICE" --no-pager
else
  echo "Deploy complete. Start your server manually from $TARGET."
fi

echo "Done."
