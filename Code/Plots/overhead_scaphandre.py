# Insert path for functions.py file
import sys
sys.path.insert(0, '{}/..'.format(sys.path[0]))

import numpy as np
import matplotlib.pyplot as plt
import json
import os

# Load power measurements and convert to array
json_string = open('Code/Plots/_log.json', 'r').read().replace('\n', '')
arr = np.array(json.loads(json_string))

# Find scaphandre PID
scaphandre_pid = 0
for measurement in arr:
    for consumer in measurement['consumers']:
        if consumer['exe'] == "scaphandre":
            scaphandre_pid = consumer['pid']
            break
if scaphandre_pid == 0:
    print("No scaphandre process found, exiting")
    exit()

start = arr[0]['host']['timestamp']

# Filter scaphandre data
from functions import filter_results
filtered = filter_results(arr, scaphandre_pid, start)

x_y = np.array(list(zip(*filtered)))

plt.figure(figsize=(10,5))
plt.plot(x_y[0], x_y[1], label="Scaphandre")
plt.ylim(0, 100)
plt.xlim(0, np.max(x_y[0]))
plt.xlabel("Time (s)")
plt.ylabel("Percentage of CPU (%)")
plt.title("CPU usage of Scaphandre")
plt.legend()
plt.savefig("Code/Plots/{}.png".format(os.path.basename(__file__).partition(".py")[0]))
plt.show()