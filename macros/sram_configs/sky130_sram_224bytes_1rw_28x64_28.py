"""
Single port, 224 byte SRAM, whole-word write. CVA6 (cv32a65x) HPDCache
directory RAM: DATA_WIDTH = $bits(hpdcache_dir_entry_t) = 4 state bits
(valid, wback, dirty, fetch) + tag(24) = 28, NUM_WORDS = sets = 64.
"""
word_size = 28 # Bits
num_words = 64
human_byte_size = "{:.0f}bytes".format((word_size * num_words)/8)

# Whole-entry writes only (directory state updates are atomic)
write_size = 28 # Bits

# Single port
num_rw_ports = 1
num_r_ports = 0
num_w_ports = 0
num_spare_rows = 1
num_spare_cols = 1
ports_human = '1rw'

import os
exec(open(os.path.join(os.path.dirname(__file__), 'sky130_sram_common.py')).read())
