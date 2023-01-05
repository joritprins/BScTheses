import numpy as np
import matplotlib.pyplot as plt
import json
import os

json_string = open('Code/_log.json', 'r').read().replace('\n', '')
arr = np.array(json.loads(json_string))
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

filtered = [
        (round(consumer['timestamp']-start, 3), round(consumer['consumption']*100/measurement['host']['consumption'])) 
            for measurement in arr 
                for consumer in measurement['consumers'] 
                    if consumer['pid'] == scaphandre_pid]

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