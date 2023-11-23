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
# write data object to disks with parities

all_write_time=[]
# different chunk size
for chunk_size in [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]:
    cfg = Config(chunk_size=chunk_size)
    dir=cfg.mkdisk('./','default')
    raid=RAID6(config=cfg,use_vm=True, debug=False)

    ## different test files
    # filename = 'test_small.txt' # 104 bytes
    # filename = 'shakespeare_small.txt' # 1145 bytes
    # filename = 'shakespeare.txt' # 5,458,199 bytes
    filename = 'img_test.png' # 1.4MB

    T_write_start = time.time()
    raid.write_to_disk(os.path.join(DATA_PATH, filename), dir)
    T_write_end = time.time()

    write_time = T_write_end-T_write_start

    print(f"write time: {write_time} seconds")
    all_write_time.append(write_time)

# for i in range(cfg.num_disk):
#     raid.vm_disk_list[i].rm_disk()
    
np.save('write_time_chunksize.npy', all_write_time)
