from src.config import Config
from src.RAID6 import RAID6
import os
from data import DATA_PATH
import time
import numpy as np

# Print the intermediate result to check the process
check=True

# Experiment start
#!------------------------ Store()
for chunk_size in [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]:
    cfg = Config(chunk_size=chunk_size)
    dir=cfg.mkdisk('./','default')
    raid=RAID6(config=cfg,use_vm=True, debug=False)

    #!------------------------ Retrieve()
    # re-ensamble data object

    T_read_start = time.time()
    restored_data = raid.retrieve('./storage_rebuild')
    T_read_end = time.time()
    # if check:
    #     print("restored data object:")
    #     print(restored_data)
    #     print('\n')

    #---------------------------
    read_time = T_read_end-T_read_start

    print(f"read time: {read_time} seconds")


