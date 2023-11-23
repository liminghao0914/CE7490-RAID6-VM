from src.config import Config
from src.RAID6 import RAID6
import os
from data import DATA_PATH
import time
import numpy as np

# Print the intermediate result to check the process
check=True

# Experiment start
all_read_time=[]
for chunk_size in [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]:
    cfg = Config(chunk_size=chunk_size)
    dir=cfg.mkdisk('./','default')
    raid=RAID6(config=cfg,use_vm=True, debug=False)

    if check:
        print("original disks:")
        original_disks = []
        for i in range(8):
            original_disks.append(raid.read_data(dir+f'/disk_{i}'))
            # print(original_disks[i])
        # print('\n')
    
    #!------------------------ Fail()
    # introduce disk failure
    raid.fail_disk(dir, 4)
    raid.fail_disk(dir, 5)

    #!------------------------ Detect()
    # detect which disks are corrupted

    fail_ids = raid.detect_failure(dir)

    #!------------------------ Rebuild()
    # restore the data and parity disks

    T_rebuild_start = time.time()
    raid.rebuild(dir, fail_ids)
    T_rebuild_end = time.time()

    if check:
        print('\n')
        print("restored disks:")
        for i in range(8):
            tmp=raid.read_data(f'./storage_rebuild/disk_{i}')
            if tmp==original_disks[i]:
                print(f"disk_{i} is correct.")
            else:
                print(f"! disk_{i} is ERROR. original len: {len(original_disks[i])} restore len: {len(tmp)}")
                print("original:")
                print(original_disks[i])
                print("restore:")
                print(tmp)
        print('\n')

    rebuild_time = T_rebuild_end-T_rebuild_start
    all_read_time.append(rebuild_time)
    print(f"rebuild time: {rebuild_time} seconds")

np.save('read_time_chunksize.npy', all_read_time)
