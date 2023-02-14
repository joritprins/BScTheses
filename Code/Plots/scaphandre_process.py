import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sp

plt.figure(figsize=(10,5))
plt.bar([2,4], [1,1], width=0.5, color='b', edgecolor='black', linewidth=.5, label='Our process')
plt.bar([0,1,3], [1,1,1], width=0.5, color='white', edgecolor='black', linewidth=.5, label='Other processes')
plt.xlabel("Jiffies", fontsize=16)
plt.legend(fontsize=20)
plt.ylim(0, 1.5)
plt.tick_params(axis='both', left=False, top=False, right=False, bottom=True, labelleft=False, labeltop=False, labelright=False, labelbottom=True, labelsize=16)
plt.savefig('scaphandre1.png')
plt.show()

data = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [9.8, 12, 10, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]]
d = sp.savgol_filter(data[1],5,2)
d = [xd - 5 for xd in d]
plt.figure(figsize=(10,5))

plt.bar([2,4,7,8], [d[2],d[4],d[7],d[8]], width=0.5, color='b', edgecolor='black', linewidth=.5, label='Our process')
plt.bar([0,1,3,5,6,9], [d[0],d[1],d[3],d[5],d[6],d[9]], width=0.5, color='white', edgecolor='black', linewidth=.5, label='Other processes')

d.insert(0, 5)
data[0].insert(0,-1)
d.insert(10, 1)
data[0].insert(11,10)
plt.plot(data[0], d, color='red', marker='o', label='Power being drawn')

plt.xlim(-.5, 9.5)
plt.tick_params(axis='both', left=False, top=False, right=False, bottom=False, labelleft=False, labeltop=False, labelright=False, labelbottom=False)
plt.xlabel('Time', fontsize=20)
plt.ylabel('Power', fontsize=20)
plt.legend(fontsize=20)

plt.savefig('scaphandre2.png')
plt.show()
