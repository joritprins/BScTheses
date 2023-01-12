# Insert path for functions.py file
import sys
sys.path.insert(0, '{}/..'.format(sys.path[0]))

import numpy as np
import matplotlib.pyplot as plt
import json
import os
from functions import filter_results

def plot(dir: str, file_names: str, runs: int, end: int):
    x_ = np.arange(0, end, 1)
    # Open file containing all PID's and save it as string
    PID_string = open('{}/pids'.format(dir), 'r').read().split("END")
    # Convert string to python dictionary
    PID_dict = json.loads("{{{}}}".format(",".join(PID_string[:-1])))
    
    interp_client = []; interp_server = []; arr = []
    for i in range(1,runs+1):
        json_string = open('{}/{}_{}.json'.format(dir, file_names, i), 'r').read().replace('\n', '')
        arr = np.array(json.loads(json_string))
    
        start = arr[0]['host']['timestamp']
        filtered_client = filter_results(arr, PID_dict[str(i)]['client'], start=start)
        filtered_server = filter_results(arr, PID_dict[str(i)]['server'], start=start)
        
        x_y_client = np.array(list(zip(*filtered_client)))
        x_y_server = np.array(list(zip(*filtered_server)))
    
        interp_client.append(np.interp(x_, x_y_client[0], x_y_client[1], left=0, right=0))
        interp_server.append(np.interp(x_, x_y_server[0], x_y_server[1], left=0, right=0))
    
    plt.figure(figsize=(10,5))
    plt.ylim(0, max(round(np.max(interp_client)), round(np.max(interp_server))))
    plt.xlim(0, end)
    plt.xlabel("Time (s)")
    plt.ylabel("Power consumption (W)")
    data = file_names.split('_')
    plt.title("Power usage of {} with {} (mean of {} runs)".format(data[0], data[1], runs))
    plt.plot(x_, np.mean(interp_client, 0), label="Client, mean: {}W, total: {}Wh".format(
                            round(np.mean(np.mean(interp_client, 0)), 3),
                            round(np.mean(np.mean(interp_client, 0)) * (end /3600), 3)))
    plt.plot(x_, np.mean(interp_server, 0), label="Server, mean: {}W, total: {}Wh".format(
                            round(np.mean(np.mean(interp_server, 0)), 3),
                            round(np.mean(np.mean(interp_server, 0)) * (end /3600), 3)))
    plt.legend()
    plt.savefig("Code/Plots/Means/{}_{}.png".format(os.path.basename(__file__).partition(".py")[0], file_names))
    return (x_, np.mean(interp_client, 0), np.mean(interp_server, 0))

xcr, cheetah_resnet50_client, cheetah_resnet50_server = plot('Code/Plots/Results/same_device/cheetah_resnet50_50', 'cheetah_resnet50', runs=50, end=256)
xcs, cheetah_sqnet_client, cheetah_sqnet_server = plot('Code/Plots/Results/same_device/cheetah_sqnet_50', 'cheetah_sqnet', runs=50, end=53)
xss, SCI_HE_sqnet_client, SCI_HE_sqnet_server = plot('Code/Plots/Results/same_device/SCI_HE_sqnet_50', 'SCI_HE_sqnet', runs=50, end=82)
xsr, SCI_HE_resnet50_client, SCI_HE_resnet50_server = plot('Code/Plots/Results/same_device/SCI_HE_resnet50_50', 'SCI_HE_resnet50', runs=50, end=560)

# Plot means of client side
plt.figure(figsize=(10,5))
# plt.ylim(0, max(
#                 max((np.max(cheetah_resnet50_client), np.max(cheetah_sqnet_client))),
#                 # max((np.max(SCI_HE_resnet50_client), np.max(SCI_HE_sqnet_client)))))
#                 np.max(SCI_HE_sqnet_server)))
# plt.xlim(0, 55)
plt.xlabel("Time (s)")
plt.ylabel("Power consumption (W)")
plt.title("Power usage of client while running sqnet")
plt.plot(xcs, cheetah_sqnet_client, 
            label="Cheetah, mean: {}W, total: {}Wh".format(
                round(np.mean(cheetah_sqnet_client), 1), 
                round(np.sum(cheetah_sqnet_client)*56/3600, 1)))
plt.plot(xss, SCI_HE_sqnet_client, 
            label="SCI_HE, mean: {}Wh, total: {}W".format(
                round(np.mean(SCI_HE_sqnet_client), 1), 
                round(np.sum(SCI_HE_sqnet_client)*83/3600, 1)))
plt.legend()
plt.savefig("Code/Plots/Means/{}_client_resnet.png".format(os.path.basename(__file__).partition(".py")[0]))

exit()

# Plot means of server side
plt.figure(figsize=(10,5))
plt.ylim(0, max(
                max((np.max(cheetah_resnet50_server), np.max(cheetah_sqnet_server))),
                # max((np.max(SCI_HE_resnet50_server), np.max(SCI_HE_sqnet_server)))))
                np.max(SCI_HE_sqnet_server)))
plt.xlim(0, 55)
plt.xlabel("Time (s)")
plt.ylabel("Power consumption (Wh)")
plt.title("Power usage of server")
plt.plot(x_, cheetah_resnet50_server, label="Cheetah resnet50")
plt.plot(x_, cheetah_sqnet_server, label="Cheetah sqnet")
plt.plot(x_, SCI_HE_sqnet_server, label="SCI_HE resnet50")
# plt.plot(x_, SCI_HE_resnet50_server, label="SCI_HE sqnet")
plt.legend()
plt.savefig("Code/Plots/Means/{}_server.png".format(os.path.basename(__file__).partition(".py")[0]))



