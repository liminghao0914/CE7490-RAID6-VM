import os
import numpy as np
import math
from os.path import join, getsize
from collections import defaultdict
import time

from .GaloisField import GaloisField
from .vm_disk import VMDisk

class RAID6(object):
    '''
    A class for RAID6 system
    Args:
        config: Config class object as configuration parameter
        debug (boolean): if the intermediate result is printed
    '''
    def __init__(self, config, use_vm=True, debug=True):
        self.debug = debug
        self.use_vm = use_vm
        self.config = config
        self.gf = GaloisField(num_data_disk = self.config.num_data_disk, num_check_disk= self.config.num_check_disk)
        self.data_disk_list  = list(range(self.config.num_data_disk))
        self.check_disk_list = list(range(self.config.num_data_disk,self.config.num_data_disk+self.config.num_check_disk))
        self.content_length = 0
        self.vm_disk_list = list(range(self.config.num_disk))
        self.rebuild_vm_disk_list = list(range(self.config.num_disk))
        print("RAID6 setup ready, ready to store data\n")  

    def read_data(self, filename, mode = 'rb'):
        '''
        Read data in the file
        Args:
            filename (str): name of the file
        Return:
            data (list)
        '''
        if self.use_vm:
            if "disk" in filename:
                if 'rebuild' in filename:
                    idx = int(filename.split('_')[-1])
                    # ! VM disk
                    data = self.rebuild_vm_disk_list[idx].read()
                    if data.status_code != 200:
                        print("Failed to read from disk {}".format(idx))
                        return []
                    else:
                        return data.json()
                else:
                    idx = int(filename.split('_')[-1])
                    # ! VM disk
                    data = self.vm_disk_list[idx].read()
                    if data.status_code != 200:
                        print("Failed to read from disk {}".format(idx))
                        return []
                    else:
                        return data.json()
        
        # Local
        with open(filename, mode) as f:
            data = list(f.read())
            if self.debug:
                print(f"read {filename}")
                print(data)
                print('\n')
            return data
    
    def distribute_data(self, filename):
        '''
        Split data in strips to different disks
        Args:
            filename (str): name of the file
        Return: 
            content: data array
        '''                
        content = self.read_data(filename)
        file_size = len(content)
        self.content_length = file_size
        padding_content=[[] for _ in range(self.config.num_data_disk)]
        
        for i in range(math.ceil(file_size/self.config.chunk_size)):
            padding_content[i%self.config.num_data_disk] = padding_content[i%self.config.num_data_disk] + list(content[i*self.config.chunk_size:min((i+1)*self.config.chunk_size,len(content))])
        
        total_stripe_number = math.ceil(file_size / self.config.stripe_size)
        
        for i in range(len(padding_content)):
            if len(padding_content[i])<self.config.chunk_size *total_stripe_number:
                padding_content[i] = list(padding_content[i]) + (self.config.chunk_size * total_stripe_number - len(padding_content[i])) * [0]
        
        padding_content = [np.array(tmp) for tmp in padding_content]
        
        content = np.concatenate(padding_content, axis=0)
        
        content = content.reshape(self.config.num_data_disk, self.config.chunk_size * total_stripe_number)
        if self.debug:
            print('file_size: ', file_size)
            print(f'distribute data into {self.config.num_data_disk} disks {len(content)} x {len(content[0])}:')
            print(content)
            print('\n')
        return content
    
    def compute_parity(self, content):
        '''
        Compute and append rows of parity data
        Args:
            content: raw data array
        Return: 
            data: array with raw data and parity data
        ''' 
        data = np.concatenate([content,self.gf.matmul(self.gf.vander, content)],axis=0)
        if self.debug:
            print("with parity: ")
            print(data)
        return data

    def chunk_save(self, data, dir):
        '''
        Distribute raw data and parity data evenly into different disks, then write into a file per disk
        Args:
            data: array with raw data and parity data
            dir: disk save directory
        ''' 
        for i in range(self.config.num_disk):
            # local disk
            if not self.use_vm:
                if os.path.exists(os.path.join(dir, 'disk_{}'.format(i))):
                    os.remove(os.path.join(dir, 'disk_{}'.format(i)))
            else:
                # ! VM disk
                if 'rebuild' in dir:
                    self.rebuild_vm_disk_list[i] = VMDisk(i, 'rebuild')
                    self.rebuild_vm_disk_list[i].rm_disk()
                else:
                    self.vm_disk_list[i] = VMDisk(i)
                    self.vm_disk_list[i].rm_disk()

        i = 0        
        parity_start_disk=0
        parity_row=self.config.num_data_disk
        data_row=0
        data_list=[[] for _ in range(self.config.num_disk)]
        while i < np.shape(data)[1]:
            parity_disks=np.arange(parity_start_disk, parity_start_disk+self.config.num_check_disk)
            parity_disks=[p%self.config.num_disk for p in parity_disks]

            if parity_row>=self.config.num_disk:
                parity_row=self.config.num_data_disk
            if data_row>=self.config.num_data_disk:
                data_row=0

            for p in parity_disks:
                data_list[p].append(data[parity_row][i:i+self.config.chunk_size])
                parity_row+=1

            for j in range(np.shape(data)[0]):
                if j not in parity_disks:
                    data_list[j].append(data[data_row][i:i+self.config.chunk_size])  
                    data_row+=1

            i=i+self.config.chunk_size
            parity_start_disk+=1

        for i in range(self.config.num_disk):
            if not self.use_vm:
                # local disk
                with open(os.path.join(dir, 'disk_{}'.format(i)), 'wb+') as f:
                    f.write(bytearray(list(np.concatenate(data_list[i]))))
            else:
                # ! VM disk
                if 'rebuild' in dir:
                    self.rebuild_vm_disk_list[i].run()
                    time.sleep(2)
                    res = self.rebuild_vm_disk_list[i].write(bytearray(list(np.concatenate(data_list[i]))))
                    if res.status_code != 200:
                        raise Exception(f'Failed to write to disk {i}')
                else:
                    self.vm_disk_list[i].run()
                    time.sleep(2)
                    res = self.vm_disk_list[i].write(bytearray(list(np.concatenate(data_list[i]))))
                    if res.status_code != 200:
                        raise Exception(f'Failed to write to disk {i}')
            
    def write_to_disk(self, filename, dir):
        data = self.distribute_data(filename)
        parity_data = self.compute_parity(data)   
        self.chunk_save(parity_data, dir)
        print("write data and parity to disk successfully\n")

    def fail_disk(self, dir, disk_number):
        # introduce disk failure by deleting the disk file
        # local disk
        if not self.use_vm:
            os.remove(os.path.join(dir,"disk_{}".format(disk_number)))
        else:
            # ! VM disk
            # res = requests.delete(f'http://{self.vm_disk_list[disk_number].ip}:5000/fail')
            res = self.vm_disk_list[disk_number].fail()
            if res.status_code != 200:
                print(res.text)
            print("disk {} failed".format(disk_number))
    
    def corrupt_disk(self, dir, disk_number):
        # introduce disk failure by mistaking parity data
        file_name = os.path.join(dir,"disk_{}".format(disk_number))
        # local disk
        if not self.use_vm:
            with open(file_name, 'rb') as f:
                content = list(f.read())  
        else:
            # ! VM disk
            content = self.read_data(file_name)
        
        content[0] = content[0]+1
        # local disk
        with open(file_name, 'wb+') as f:
            f.write(bytearray(content))
        # ! VM disk
        

    def detect_failure(self, dir):
        # detect which disk is corrupted 
        fail_ids = []
        for disk_number in range(self.config.num_disk):
            # local disk
            if not self.use_vm:
                file_name = os.path.join(dir,"disk_{}".format(disk_number))
                if not os.path.exists(file_name):
                    print("detected disk {} failture".format(disk_number))
                    fail_ids.append(disk_number)
            else:
                # ! VM disk
                # res = requests.get(f'http://{self.vm_disk_list[disk_number].ip}:5000/detect')
                if 'rebuild' in dir:
                    res = self.rebuild_vm_disk_list[disk_number].detect()
                else:
                    res = self.vm_disk_list[disk_number].detect()
                if res.text == 'False':
                    fail_ids.append(disk_number)
        return fail_ids

    def rebuild(self, dir, fail_ids):
        '''
        Compute original data array by matrix inversion after removing corrupted rows
        Args:
            dir (str): input disk directory
            fail_ids (list): detected id of failed disks
        ''' 
        n = len(fail_ids)
        if n > self.config.num_check_disk:
            print("\n","ERROR: too many failed disks.", "\n")
            return -1

        chunks_restore = []
        all_disks = defaultdict(lambda: None)
        
        if not self.use_vm:
            # local disk
            for d in os.listdir(dir):
                all_disks[int(d.split("_")[-1])]=self.read_data(dir+'/'+d)
        else:
            # ! VM disk
            for i in range(self.config.num_disk):
                all_disks[i] = self.read_data(f'disk_{i}')
        assert(len(all_disks[list(all_disks.keys())[0]])%self.config.chunk_size==0)
        n_chunks = int(len(all_disks[0])/self.config.chunk_size)

        parity_start_disk=0
        for i in range(n_chunks):
            parity_disks=np.arange(parity_start_disk, parity_start_disk+self.config.num_check_disk)
            parity_disks=[p%self.config.num_disk for p in parity_disks]

            F = self.gf.vander
            I = np.identity(self.config.num_data_disk)
            A = np.concatenate((I,F))

            E_remove = []
            for j in range(self.config.num_disk):
                if j not in fail_ids:
                    if j not in parity_disks:
                        E_remove.append(all_disks[j][i*self.config.chunk_size:(i+1)*self.config.chunk_size])

            for z in parity_disks:
                if z not in fail_ids:
                    E_remove.append(all_disks[z][i*self.config.chunk_size:(i+1)*self.config.chunk_size])
            
            remian_rows = []
            id = 0
            # add remaining data rows
            for m in range(self.config.num_disk):
                if m not in fail_ids and m not in parity_disks:
                    remian_rows.append(id)
                if m not in parity_disks:
                    id+=1
            # add remaining parity rows
            parity_row=self.config.num_data_disk
            for x in parity_disks:
                if x not in fail_ids:
                    remian_rows.append(parity_row)
                parity_row+=1

            A_remove = A[remian_rows,:]
            A_r_inv = self.gf.gf_inverse(np.array(A_remove,dtype=int))
            D = self.gf.matmul(A_r_inv,np.array(E_remove,dtype=int))
            chunks_restore.append(D.tolist())

            parity_start_disk += 1

        data_restore = [[] for _ in range (self.config.num_data_disk)]
        for c in range(n_chunks):
            for l in range(self.config.num_data_disk):
                data_restore[l].extend(chunks_restore[c][l])
        
        parity_data_restore = self.compute_parity(np.array(data_restore))
        
        if not self.use_vm:
            # local disk
            dir_rebuild=self.config.mkdisk('./','rebuild')
        else:
            # ! VM disk
            dir_rebuild = './storage_rebuild'
        self.chunk_save(parity_data_restore, dir_rebuild)
        return

    def retrieve(self, dir):
        '''
        Remove parity data and ensamble data strips for original data object
        Args:
            dir (str): disk directory
        ''' 
        fail_ids = self.detect_failure(dir)
        if len(fail_ids)>0:
            raise Exception("Sorry, storage disks are damaged.")

        chunks_restore = []
        all_disks = defaultdict(lambda: None)
        if not self.use_vm:
            # local disk
            for d in os.listdir(dir):
                all_disks[int(d.split("_")[-1])]=self.read_data(dir+'/'+d)
        else:
            # ! VM disk
            for i in range(self.config.num_disk):
                all_disks[i] = self.read_data(f'{dir}/disk_{i}')

        n_chunks = int(len(all_disks[0])/self.config.chunk_size)

        parity_start_disk=0
        remove_parity = []
        for i in range(n_chunks):
            parity_disks=np.arange(parity_start_disk, parity_start_disk+self.config.num_check_disk)
            parity_disks=[p%self.config.num_disk for p in parity_disks]

            remove_parity_chunk = []
            for j in range(self.config.num_disk):
                if j not in parity_disks:
                   remove_parity_chunk.append(all_disks[j][i*self.config.chunk_size:(i+1)*self.config.chunk_size]) 
            remove_parity.append(remove_parity_chunk)
            parity_start_disk += 1

        data_retrieve = []
        for h in range(n_chunks):
            for v in range(self.config.num_data_disk):
                arr = remove_parity[h][v]
                data_retrieve.extend(arr)
        data_retrieve = data_retrieve[:self.content_length]
        data_retrieve = bytearray(data_retrieve)

        #open text file
        text_file = open("data_retrieved", "wb")        
        #write string to file
        text_file.write(data_retrieve)
        #close file
        text_file.close()

        return data_retrieve

