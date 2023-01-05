import numpy as np
import matplotlib.pyplot as plt
import json
import os

x_ = np.arange(0, 65, 0.1)
results = []

plt.figure(figsize=(10,5))

for i in range(1,9):
    json_string = open('Code/Plots/Cheetah_sqnet_10/cheetah_sqnet_{}.json'.format(i), 'r').read().replace('\n', '')
    arr = np.array(json.loads(json_string))

    # Find PID of scaphandre
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
    print(np.min(x_y[0]),np.max([x_y[0]]))
    plt.plot(x_y[0], x_y[1], label="Scaphandre (run {})".format(i))

    results.append(np.interp(x_, x_y[0], x_y[1]))

plt.ylim(0, 100)
plt.xlim(0, np.max(x_y[0]))
plt.xlabel("Time (s)")
plt.ylabel("Percentage of total power (%)")
plt.title("CPU usage of Scaphandre")
plt.legend()
plt.savefig("Code/Plots/{}.png".format(os.path.basename(__file__).partition(".py")[0]))
plt.show()

print(len(np.mean(results, 0)))
plt.plot(x_, np.mean(results, 0))
plt.show()


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