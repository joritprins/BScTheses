# Insert path for functions.py file
import sys
sys.path.insert(0, '{}/..'.format(sys.path[0]))

import numpy as np
import matplotlib.pyplot as plt
import json
import os
from functions import filter_results

results = []

plt.figure(figsize=(10,5))

# Open file containing all PID's and save it as string
PID_string = open('Code/Plots/Cheetah_sqnet_10/pids', 'r').read().split("END")
# Convert string to python dictionary
PID_dict = json.loads("{{{}}}".format(",".join(PID_string[:-1])))

interp_client = []; interp_server =[]

runs = 4
for i in range(0,runs):
    json_string = open('Code/Plots/Cheetah_sqnet_10/cheetah_sqnet_{}.json'.format(i), 'r').read().replace('\n', '')
    arr = np.array(json.loads(json_string))    
    start = arr[0]['host']['timestamp']

    filtered_client = filter_results(arr, PID_dict[str(i)]['client'], start=start)
    filtered_server = filter_results(arr, PID_dict[str(i)]['server'], start=start)
    
    x_y_client = np.array(list(zip(*filtered_client)))
    x_y_server = np.array(list(zip(*filtered_server)))

    x_ = np.arange(0, x_y_client[0][-1], x_y_client[0][-1]/1000)
    interp_client.append(np.interp(x_, x_y_client[0], x_y_client[1]))
    x_ = np.arange(0, x_y_server[0][-1], x_y_server[0][-1]/1000)
    interp_server.append(np.interp(x_, x_y_server[0], x_y_server[1]))

plt.ylim(0, max(np.max(interp_client), np.max(interp_server)))
plt.xlabel("Time (s)")
plt.ylabel("Power consumption (Wh)")
plt.title("Power usage after {} runs".format(runs))
x_ = np.arange(0, 100, 0.1)
plt.plot(x_, np.mean(interp_client, 0), label="Client")
plt.plot(x_, np.mean(interp_server, 0), label="Server")
plt.legend()
# plt.savefig("Code/Plots/{}.png".format(os.path.basename(__file__).partition(".py")[0]))
plt.show()