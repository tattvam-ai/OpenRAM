"""
Single port, 1 kbyte SRAM, whole-word write. CVA6 (cv32a65x) icache data RAM:
DATA_WIDTH = ICACHE_LINE_WIDTH = 128, NUM_WORDS = ICACHE_NUM_WORDS = 64,
BYTE_ACCESS(0) -- whole cacheline written at once, no byte masking.
"""
word_size = 128 # Bits
num_words = 64
human_byte_size = "{:.0f}kbytes".format((word_size * num_words)/1024/8)

# Whole-word writes only (icache BYTE_ACCESS = 0)
write_size = 128 # Bits

# Single port
num_rw_ports = 1
num_r_ports = 0
num_w_ports = 0
num_spare_rows = 1
num_spare_cols = 1
words_per_row = 2  # avoids a supply-router pathfinding failure at the natural 64x128 aspect ratio
ports_human = '1rw'

import os
exec(open(os.path.join(os.path.dirname(__file__), 'sky130_sram_common.py')).read())
