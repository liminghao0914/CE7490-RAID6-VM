import time
import os
import shutil

class Config(object):
    '''
    RAID6 initialization configuration
    Args:
        num_disk: total disk count
        num_data_disk: disk for data storage
        num_check_disk: disk for parity storage
    '''
    def __init__(self, num_disk=8, num_data_disk=6, num_check_disk=2, chunk_size=256):
        self.num_disk = num_disk
        self.num_data_disk = num_data_disk
        self.num_check_disk = num_check_disk

        assert self.num_disk == self.num_data_disk + self.num_check_disk

        self.chunk_size = chunk_size
        self.stripe_size = self.num_data_disk * self.chunk_size
        
        print("\nNum of Disk: %d" % self.num_disk)
        print("Num of Data Disk: %d" % self.num_data_disk)
        print("Num of Checksum: %d" % self.num_check_disk)
        print("RAID-6 configuration initialized\n")
    
    def mkdisk(self, root, experiment_name):
        '''
        Make test directory for disk
        return: 
            test_dir: test folder directory
        '''
        test_dir = os.path.join(root, f'storage_{experiment_name}')
        if os.path.isdir(test_dir):
            shutil.rmtree(test_dir)
        os.mkdir(test_dir)
        return test_dir
    