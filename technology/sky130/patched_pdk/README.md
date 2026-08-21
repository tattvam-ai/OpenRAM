# Locally patched sky130A ngspice models

This directory is a copy of `$PDK_ROOT/sky130A/{libs.tech/ngspice,libs.ref/sky130_fd_pr/spice}`,
used **only** for OpenRAM's SPICE-based (`analytical_delay = False`) characterization.
`$PDK_ROOT` itself is never modified.

## Why this exists

The sky130 SRAM bitcell (`sky130_fd_bd_sram__sram_sp_cell_opt1{,a}` and its
replica/dummy variants) uses the PDK's narrow-width "special" transistor
models. Two independent bugs in how the vendored PDK ngspice files define
these models block ngspice (tested: ngspice-45, `ngbehavior=hsa`) from
resolving them at all -- with or without OpenRAM's local sky130 DRC/LVS
fixes, and reproducible in a 3-line netlist with no OpenRAM code involved.

1. **Model-card name mismatch.** In `sky130_fd_pr__special_{p,n}fet_latch.pm3.spice`
   and `sky130_fd_pr__special_nfet_pass.pm3.spice`, the MOSFET instance line
   references the bare model name (e.g. `sky130_fd_pr__special_pfet_latch__model`),
   but the actual `.model` card is named with a stray bin suffix
   (`sky130_fd_pr__special_pfet_latch__model.0`). There is no second bin for
   nfet, and for pfet only bin 0 (L~0.15um, W~0.14um) is ever actually used
   by any bitcell variant OpenRAM's `sky130_bitcell.py` selects (`opt1`/`opt1a`
   and their replica/dummy counterparts) -- bin 1 and the L=0.095um instances
   found in unused cell variants (plain `sram_sp_cell`, `*_opt1_ce`) are not
   part of this fix.
   **Fix:** dropped the `.0` suffix from the bin-0 `.model` card name in
   `sky130_fd_pr__special_pfet_latch.pm3.spice` (line 35),
   `sky130_fd_pr__special_nfet_latch.pm3.spice` (line 34), and
   `sky130_fd_pr__special_nfet_pass.pm3.spice` (line 34).

2. **Broken legacy-name wrapper.** `sky130_fd_pr__special_pfet_latch.pm3.spice`
   also defines `sky130_fd_pr__special_pfet_pass` as a thin pass-through
   wrapper to `special_pfet_latch`, per the file's own comment: *"special_pfet_pass
   was incorrect nomenclature and has been fixed to special_pfet_latch. The
   original incorrect name is kept here to prevent breaking legacy netlists."*
   ngspice fails to resolve the nested subcircuit call inside this wrapper
   (`Error: unknown subckt: ... sky130_fd_pr__special_pfet_latch`), even
   after fix #1 above and even in complete isolation -- root cause not fully
   determined (an instance-name-collision theory was tested and ruled out).
   **Fix:** rather than debug ngspice's internals further, bypassed the
   wrapper entirely: every *active* (non-commented) call site in
   `../sp_lib/*.sp` that referenced `sky130_fd_pr__special_pfet_pass` was
   changed to call `sky130_fd_pr__special_pfet_latch` directly, which is
   documented by the PDK itself to be electrically identical. Commented-out
   call sites (dead code, e.g. the L=0.095um instances) were left untouched.
   No `special_nfet_pass` calls needed to change -- it is a real, independent
   device (its own file, own characterization), not an alias, and once fix #1
   is applied it resolves directly with no wrapper involved.

Both bugs were confirmed with minimal standalone ngspice reproductions
(no OpenRAM code) before being attributed to the PDK rather than OpenRAM.

## Regenerating this directory

```
rm -rf technology/sky130/patched_pdk
mkdir -p technology/sky130/patched_pdk/libs.tech technology/sky130/patched_pdk/libs.ref/sky130_fd_pr
cp -r "$PDK_ROOT/sky130A/libs.tech/ngspice" technology/sky130/patched_pdk/libs.tech/ngspice
cp -r "$PDK_ROOT/sky130A/libs.ref/sky130_fd_pr/spice" technology/sky130/patched_pdk/libs.ref/sky130_fd_pr/spice
```
Then re-apply the two model-card renames and the `special_pfet_pass` ->
`special_pfet_latch` sp_lib substitution described above.

`technology/sky130/__init__.py` automatically prefers this directory over
`$PDK_ROOT` for `SPICE_MODEL_DIR` when it's present; delete it to fall back
to the unpatched PDK (DRC/LVS/GDS are unaffected either way -- they don't
use this directory).
