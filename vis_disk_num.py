import matplotlib.pyplot as plt
import numpy as np
import os

# Plot the disknum vs. read time
vm_files = os.listdir('./saved/vmdisk/')
local_files = os.listdir('./saved/localdisk/')

chunk_size_x = []
read_time_y = []
for file in vm_files:
    if file.startswith('chunk_size_256_num_disk') and 'txt' not in file:
        data = np.load('./saved/vmdisk/'+file)
        chunk_size = int(file.split('_')[5])
        read_time = data['read_time']
        chunk_size_x.append(chunk_size)
        read_time_y.append(read_time)
chunk_size_x = sorted(chunk_size_x)
read_time_y = sorted(read_time_y)
plt.plot(chunk_size_x, read_time_y, 'o-', linewidth=2, label='VM Disk')

chunk_size_x = []
read_time_y = []
for file in local_files:
    if file.startswith('chunk_size_256_num_disk') and 'txt' not in file:
        data = np.load('./saved/localdisk/'+file)
        chunk_size = int(file.split('_')[5])
        read_time = data['read_time']
        chunk_size_x.append(chunk_size)
        read_time_y.append(read_time)
chunk_size_x = sorted(chunk_size_x)
read_time_y = sorted(read_time_y)
plt.plot(chunk_size_x, read_time_y, 'o-', linewidth=2, label='Local Disk')

# plt.xticks(chunk_size_x, [r'$2^{%d}$' % i for i in chunk_size_x])
plt.xlabel('Disk Num', fontsize=18)
plt.ylabel('Read Time (s)', fontsize=18)
plt.grid()
plt.legend(fontsize=18, loc='upper left')
plt.savefig('imgs/read_time_disknum.pdf')
# clear the figure
plt.clf()


chunk_size_x = []
write_time_y = []
for file in vm_files:
    if file.startswith('chunk_size_256_num_disk') and 'txt' not in file:
        data = np.load('./saved/vmdisk/'+file)
        chunk_size = int(file.split('_')[5])
        write_time = data['write_time']
        chunk_size_x.append(chunk_size)
        write_time_y.append(write_time)
chunk_size_x = sorted(chunk_size_x)
write_time_y = sorted(write_time_y)
plt.plot(chunk_size_x, write_time_y, 'o-', linewidth=2, label='VM Disk')

chunk_size_x = []
write_time_y = []
for file in local_files:
    if file.startswith('chunk_size_256_num_disk') and 'txt' not in file:
        data = np.load('./saved/localdisk/'+file)
        chunk_size = int(file.split('_')[5])
        write_time = data['write_time']
        chunk_size_x.append(chunk_size)
        write_time_y.append(write_time)
chunk_size_x = sorted(chunk_size_x)
write_time_y = sorted(write_time_y)
plt.plot(chunk_size_x, write_time_y, 'o-', linewidth=2, label='Local Disk')

# plt.xticks(chunk_size_x, [r'$2^{%d}$' % i for i in chunk_size_x])
plt.xlabel('Disk Num', fontsize=18)
plt.ylabel('Write Time (s)', fontsize=18)
plt.grid()
plt.legend(fontsize=18, loc='upper left')
plt.savefig('imgs/write_time_disknum.pdf')
# clear the figure
plt.clf()

chunk_size_x = []
rebuild_time_y = []
for file in vm_files:
    if file.startswith('chunk_size_256_num_disk') and 'txt' not in file:
        data = np.load('./saved/vmdisk/'+file)
        chunk_size = int(file.split('_')[5])
        rebuild_time = data['rebuild_time']
        chunk_size_x.append(chunk_size)
        rebuild_time_y.append(rebuild_time)
chunk_size_x = sorted(chunk_size_x)
rebuild_time_y = sorted(rebuild_time_y)
plt.plot(chunk_size_x, rebuild_time_y, 'o-', linewidth=2, label='VM Disk')

chunk_size_x = []
rebuild_time_y = []
for file in local_files:
    if file.startswith('chunk_size_256_num_disk') and 'txt' not in file:
        data = np.load('./saved/localdisk/'+file)
        chunk_size = int(file.split('_')[5])
        rebuild_time = data['rebuild_time']
        chunk_size_x.append(chunk_size)
        rebuild_time_y.append(rebuild_time)
chunk_size_x = sorted(chunk_size_x)
rebuild_time_y = sorted(rebuild_time_y)
plt.plot(chunk_size_x, rebuild_time_y, 'o-', linewidth=2, label='Local Disk')

plt.xticks(chunk_size_x, [r'$2^{%d}$' % i for i in chunk_size_x])
plt.xlabel('Disk Num', fontsize=18)
plt.ylabel('Rebuild Time (s)', fontsize=18)
plt.grid()
plt.legend(fontsize=18, loc='upper left')
plt.savefig('imgs/rebuild_time_disknum.pdf')