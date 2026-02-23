#!/usr/bin/env bash
# Hook PostToolUse - Documentation change tracker
# Detecte les modifications de fichiers source et enregistre les docs impactees
# Doit s'executer en < 500ms (pas de jq, pas de Python)
set -euo pipefail

# Lire stdin (JSON de l'outil)
INPUT=$(cat)

# Extraction rapide sans jq (performance)
TOOL_NAME=$(echo "$INPUT" | grep -oP '"tool_name"\s*:\s*"[^"]*"' | head -1 | grep -oP ':\s*"\K[^"]*' || true)

# Seuls Write et Edit nous interessent
if [[ "$TOOL_NAME" != "Write" && "$TOOL_NAME" != "Edit" ]]; then
  exit 0
fi

# Extraire le file_path
FILE_PATH=$(echo "$INPUT" | grep -oP '"file_path"\s*:\s*"[^"]*"' | head -1 | grep -oP ':\s*"\K[^"]*' || true)

if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

# Chemin relatif depuis la racine du projet
PROJECT_ROOT="/home/plc/haraspilot"
REL_PATH="${FILE_PATH#$PROJECT_ROOT/}"

# Ne pas tracker les docs elles-memes, tests, node_modules, configs Claude
case "$REL_PATH" in
  docs/*|*__tests__*|*.test.*|node_modules/*|.claude/*|_bmad/*|*.md)
    exit 0
    ;;
esac

# Ne tracker que les fichiers source
case "$REL_PATH" in
  *.ts|*.tsx|*.rs|*.astro|*.json)
    ;;
  *)
    exit 0
    ;;
esac

# Ignorer tauri.conf.json et package.json (trop de bruit)
case "$REL_PATH" in
  */package.json|*/package-lock.json|*/tsconfig.json)
    exit 0
    ;;
esac

# Tracker le changement
TRACKER_DIR="$PROJECT_ROOT/docs/_tracker"
TRACKER_FILE="$TRACKER_DIR/pending-changes.jsonl"

mkdir -p "$TRACKER_DIR"

# Append atomique
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"file\":\"$REL_PATH\",\"tool\":\"$TOOL_NAME\"}" >> "$TRACKER_FILE"
