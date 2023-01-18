# Insert path for functions.py file
import sys
sys.path.insert(0, '{}/..'.format(sys.path[0]))

import numpy as np
import matplotlib.pyplot as plt
import json
import os
from functions import filter_results

def plot(dir: str, runs: int, end: int):
    x_ = np.arange(0, end, 0.1)
    
    interp_client = []; interp_server = []
    for i in range(1,runs+1):
        pid_client = 0; pid_server = 0
        json_string = open('{}/client_{}.json'.format(dir, i), 'r').read().replace('\n', '')
        arr_client = np.array(json.loads(json_string))
        for measurement in arr_client:
            for consumer in measurement['consumers']:
                if consumer['exe'] == 'sqnet-cheetah':
                    pid_client = consumer['pid']
        
        json_string = open('{}/server_{}.json'.format(dir, i), 'r').read().replace('\n', '')
        arr_server = np.array(json.loads(json_string))
        for measurement in arr_server:
            for consumer in measurement['consumers']:
                if consumer['exe'] == 'sqnet-cheetah':
                    pid_server = consumer['pid']

        start_c = arr_client[0]['host']['timestamp']
        start_s = arr_server[0]['host']['timestamp']
        start = start_c if start_c < start_s else start_s
        filtered_client = filter_results(arr_client, pid_client, start=start)
        filtered_server = filter_results(arr_server, pid_server, start=start)
        
        x_y_client = np.array(list(zip(*filtered_client)))
        x_y_server = np.array(list(zip(*filtered_server)))
    
        interp_client.append(np.interp(x_, x_y_client[0], x_y_client[1], left=0, right=0))
        interp_server.append(np.interp(x_, x_y_server[0], x_y_server[1], left=0, right=0))
    
    plt.figure(figsize=(10,5))
    plt.ylim(0, max(round(np.max(interp_client)), round(np.max(interp_server))))
    plt.xlim(0, end)
    plt.xlabel("Time (s)")
    plt.ylabel("Power consumption (W)")
    data = dir.split('/')[-1].split('_')
    plt.title("Power usage of {} with {} (mean of {} runs)".format(data[0], data[1], runs))
    plt.plot(x_, np.mean(interp_client, 0), label="Client, mean: {}W, total: {}Wh".format(
                            round(np.mean(np.mean(interp_client, 0)), 3),
                            round(np.mean(np.mean(interp_client, 0)) * (end /3600), 3)))
    plt.plot(x_, np.mean(interp_server, 0), label="Server, mean: {}W, total: {}Wh".format(
                            round(np.mean(np.mean(interp_server, 0)), 3),
                            round(np.mean(np.mean(interp_server, 0)) * (end /3600), 3)))
    plt.legend()
    plt.savefig("Code/Plots/Means/{}_{}_{}.png".format(os.path.basename(__file__).partition(".py")[0], data[1], data[0]))
    return (x_, np.mean(interp_client, 0), np.mean(interp_server, 0))

xcr, csc, css = plot('Code/Plots/Results/laptop_desktop/cheetah_sqnet', runs=10, end=115)
exit()
# Plot means of client side
plt.figure(figsize=(10,5))
# plt.ylim(0, max(
#                 max((np.max(cheetah_resnet50_client), np.max(cheetah_sqnet_client))),
#                 # max((np.max(SCI_HE_resnet50_client), np.max(SCI_HE_sqnet_client)))))
#                 np.max(SCI_HE_sqnet_server)))
# plt.xlim(0, 55)
plt.xlabel("Time (s)")
plt.ylabel("Power consumption (Wh)")
plt.title("Power usage of client while running sqnet")
plt.plot(xcs, cheetah_sqnet_client, 
            label="Cheetah, mean: {}Wh, total: {}W".format(
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



