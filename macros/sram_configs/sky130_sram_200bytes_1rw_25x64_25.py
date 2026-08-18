"""
Single port, 200 byte SRAM, whole-word write. CVA6 (cv32a65x) icache tag+valid
RAM: DATA_WIDTH = ICACHE_TAG_WIDTH(24) + valid(1) = 25, NUM_WORDS =
ICACHE_NUM_WORDS = 64, BYTE_ACCESS(0).
"""
word_size = 25 # Bits
num_words = 64
human_byte_size = "{:.0f}bytes".format((word_size * num_words)/8)

# Whole-word writes only (icache BYTE_ACCESS = 0)
write_size = 25 # Bits

# Single port
num_rw_ports = 1
num_r_ports = 0
num_w_ports = 0
num_spare_rows = 1
num_spare_cols = 0  # word_size (25) is odd, so no spare column is needed for the sky130 column-parity rule
words_per_row = 1  # avoids a supply-router pathfinding failure at the natural 32x50 aspect ratio
ports_human = '1rw'

import os
exec(open(os.path.join(os.path.dirname(__file__), 'sky130_sram_common.py')).read())
