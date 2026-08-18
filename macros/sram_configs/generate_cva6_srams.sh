#!/bin/bash
# Generate the sky130 SRAM macros needed for CVA6 (cv32a65x config, as built
# by OpenROAD-flow-scripts) -- icache tag+data and dcache (HPDCache)
# directory+data arrays. See the docstring in each config file under
# sram_configs/ for how its dimensions were derived from the CVA6 RTL.
#
# Usage (from the repo root):
#   ./macros/sram_configs/generate_cva6_srams.sh
#
# Requires PDK_ROOT to point at a sky130 PDK installed via `make sky130-pdk`
# and `make sky130-install` (see docs/source/basic_setup.md). Defaults to
# $HOME/openram_pdk_root if PDK_ROOT is not already set.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

export OPENRAM_HOME="$REPO_ROOT/compiler"
export OPENRAM_TECH="$REPO_ROOT/technology"
export PDK_ROOT="${PDK_ROOT:-$HOME/openram_pdk_root}"

CONFIGS=(
  sky130_sram_1kbyte_1rw_64x128_8    # D$ (HPDCache) data RAM
  sky130_sram_1kbyte_1rw_128x64_128  # I$ data RAM
  sky130_sram_200bytes_1rw_25x64_25  # I$ tag+valid RAM
  sky130_sram_224bytes_1rw_28x64_28  # D$ (HPDCache) directory RAM
)

for cfg in "${CONFIGS[@]}"; do
  echo "=== Generating $cfg ==="
  nix --extra-experimental-features 'nix-command flakes' develop --command \
    python3 sram_compiler.py -v "macros/sram_configs/${cfg}.py"
done

echo
echo "Done. Outputs are in macro/<name>/ (GDS, LEF, SPICE, Liberty, Verilog)."
echo "Check each run's output for these lines to confirm sign-off:"
echo "  KLayout DRC (sky130A ruleset): 0 violation(s)"
echo "  <name>  LVS matches"
