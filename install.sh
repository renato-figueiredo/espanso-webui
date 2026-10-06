#!/usr/bin/env bash
# Instala o comando `espanso-webui` em ~/.local/bin (link simbólico para este diretório).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$HOME/.local/bin"
chmod +x "$here/espanso-webui"
ln -sf "$here/espanso-webui" "$HOME/.local/bin/espanso-webui"
python3 -c "import yaml" 2>/dev/null || echo "Aviso: falta PyYAML (pip install --user pyyaml ou o pacote python3-yaml)."
echo "Pronto. Rode: espanso-webui"
