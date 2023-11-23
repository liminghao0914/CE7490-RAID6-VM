from raidvm.config import Config
from raidvm.RAID6 import RAID6
import os
from data import DATA_PATH
import time
import numpy as np


def run(args):
    # Print the intermediate result to check the process
    check=True
    
    # Experiment start
    cfg = Config(num_disk=args.num_disk, chunk_size=args.chunk_size)
    dir=cfg.mkdisk('./','default')
    raid=RAID6(config=cfg,use_vm=args.use_vm, debug=False)

    ## different test files
    # filename = 'test_small.txt' # 104 bytes
    # filename = 'shakespeare_small.txt' # 1145 bytes
    # filename = 'shakespeare.txt' # 5,458,199 bytes
    # filename = 'img_test.png' # 1.4MB
    filename = args.filename


    #! Store()
    # write data object to disks with parities
    T_write_start = time.time()
    raid.write_to_disk(os.path.join(DATA_PATH, filename), dir)
    T_write_end = time.time()
    
    if check:
        print("original disks:")
        original_disks = []
        for i in range(8):
            original_disks.append(raid.read_data(dir+f'/disk_{i}'))
            # print(original_disks[i])
        print('\n')

    #! Fail()
    # introduce disk failure
    raid.fail_disk(dir, 4)
    raid.fail_disk(dir, 5)

    #! Detect()
    # detect which disks are corrupted
    fail_ids = raid.detect_failure(dir)

    #! Rebuild()
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

    #! Retrieve()
    # re-ensamble data object

    T_read_start = time.time()
    restored_data = raid.retrieve('./storage_rebuild')
    T_read_end = time.time()
    # if check:
    #     print("restored data object:")
    #     print(restored_data)
    #     print('\n')

    read_time = T_read_end-T_read_start
    write_time = T_write_end-T_write_start
    rebuild_time = T_rebuild_end-T_rebuild_start

    print(f"read time: {read_time} seconds")
    print(f"write time: {write_time} seconds")
    print(f"rebuild time: {rebuild_time} seconds")
    if args.use_vm:
        np.savez(f'saved/vmdisk/chunk_size_{args.chunk_size}_num_disk_{args.num_disk}_time.npz', read_time=read_time, write_time=write_time, rebuild_time=rebuild_time)
    else:
        np.savez(f'saved/localdisk/chunk_size_{args.chunk_size}_num_disk_{args.num_disk}_time.npz', read_time=read_time, write_time=write_time, rebuild_time=rebuild_time)
    
    if args.use_vm:
        print("cleaning up...")
        for i in range(cfg.num_disk):
            raid.vm_disk_list[i].rm_disk()
            raid.rebuild_vm_disk_list[i].rm_disk()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--chunk_size', type=int, default=256)
    parser.add_argument('--num_disk', type=int, default=8)
    parser.add_argument('--use_vm', action='store_true')
    parser.add_argument('--filename', type=str, default='img_test.png')
    args = parser.parse_args()
    
    run(args)
