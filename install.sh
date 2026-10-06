#!/usr/bin/env bash
# Installs the `espanso-webui` command into ~/.local/bin (symlink to this directory).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$HOME/.local/bin"
chmod +x "$here/espanso-webui"
ln -sf "$here/espanso-webui" "$HOME/.local/bin/espanso-webui"
python3 -c "import yaml" 2>/dev/null || echo "Warning: PyYAML is missing (pip install --user pyyaml or your distro's python3-yaml package)."
echo "Done. Run: espanso-webui"
