"""
Single port, 1 kbyte SRAM, with byte write. CVA6 (cv32a65x) HPDCache data RAM:
DATA_RAM_WIDTH = dataWaysPerRamWord(2) x wordWidth(32) = 64,
DATA_RAM_DEPTH = sets(64) x (clWords(4)/accessWords(2)) = 128, byte-enabled writes.
"""
word_size = 64 # Bits
num_words = 128
human_byte_size = "{:.0f}kbytes".format((word_size * num_words)/1024/8)

# Byte-enabled writes (HPDCache dataRamByteEnable=1)
write_size = 8 # Bits

# Single port
num_rw_ports = 1
num_r_ports = 0
num_w_ports = 0
num_spare_rows = 1
num_spare_cols = 1
ports_human = '1rw'

import os
exec(open(os.path.join(os.path.dirname(__file__), 'sky130_sram_common.py')).read())
