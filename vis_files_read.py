import matplotlib.pyplot as plt
import numpy as np
import os

# Plot the disknum vs. read time
vm_files = os.listdir('./saved/vmdisk/')
local_files = os.listdir('./saved/localdisk/')
barWidth = 0.3

fig, ax = plt.subplots(layout='constrained')
vm_file_x = []
vm_read_time_y = []
for file in vm_files:
    if file.startswith('chunk_size_256_num_disk_8_') and 'jpeg' in file:
        data = np.load('./saved/vmdisk/'+file)
        filename = file.split('_')[6]
        read_time = data['read_time']
        vm_file_x.append(filename)
        vm_read_time_y.append(read_time)
vm_read_time_y = sorted(vm_read_time_y)

local_file_x = []
local_read_time_y = []
for file in local_files:
    if file.startswith('chunk_size_256_num_disk_8_') and 'jpeg' in file:
        data = np.load('./saved/localdisk/'+file)
        filename = file.split('_')[6]
        read_time = data['read_time']
        local_file_x.append(filename)
        local_read_time_y.append(read_time)
local_read_time_y = sorted(local_read_time_y)

species = ['500kb','1mb','2mb','5mb','10mb','15mb','20mb']
penguin_means = {
    'VM Disk': vm_read_time_y,
    'Local Disk': local_read_time_y
}


x = np.arange(len(species))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in penguin_means.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('read Time (s)', fontsize=18)
ax.set_xlabel('File Size', fontsize=18)
# set_xlabel font size

ax.set_xticks(x + width, species)
ax.legend(loc='upper left', ncols=3, fontsize=18)
# ax.set_ylim(0, 250)

plt.savefig('imgs/read_time_files.pdf')
# clear the figure
plt.clf()