# Insert path for functions.py file
import sys
sys.path.insert(0, '{}/..'.format(sys.path[0]))
sys.path.insert(0, '{}/../..'.format(sys.path[0]))

import numpy as np
import matplotlib.pyplot as plt
import json
import os
from functions import filter_results

# def plot(dir: str, file_names: str, runs: int, end: int, size=(int, int)):
#     """
#     Plot the file in dir with name file_names

#     dir         : name of the dir that the files are in
#     file_names  : base of the file names
#     runs        : determines how many files there are -> files go from 1 till runs+1
#     end         : this script will interpolate the results from 0 till end

#     returns the interpolated client and server results
#     """
#     x_ = np.arange(0, end, .1)
#     # Open file containing all PID's and save it as string
#     PID_string = open('{}/pids'.format(dir), 'r').read().split("END")
#     # Convert string to python dictionary
#     PID_dict = json.loads("{{{}}}".format(",".join(PID_string[:-1])))
    
#     interp_client = []; interp_server = []; arr = []
#     for i in range(1,runs+1):
#         # Readd files and convert to numpy array
#         json_string = open('{}/{}-{}.json'.format(dir, file_names, i), 'r').read().replace('\n', '')
#         arr = np.array(json.loads(json_string))

#         # Filter results
#         start = arr[0]['host']['timestamp']
#         filtered_client = filter_results(arr, PID_dict[str(i)]['client'], start=start)
#         filtered_server = filter_results(arr, PID_dict[str(i)]['server'], start=start)
        
#         x_y_client = np.array(list(zip(*filtered_client)))
#         x_y_server = np.array(list(zip(*filtered_server)))
    
#         interp_client.append(np.interp(x_, x_y_client[0], x_y_client[1], left=0, right=0))
#         interp_server.append(np.interp(x_, x_y_server[0], x_y_server[1], left=0, right=0))
    
#     plt.figure(figsize=(10,5))
#     plt.ylim(0, max(round(np.max(interp_client)), round(np.max(interp_server))))
#     plt.xlim(0, end)
#     plt.xlabel("Time (s)")
#     plt.ylabel("Power consumption (W)")
#     data = file_names.split('-')
#     plt.title("Power usage of {} with {} (mean of {} runs)".format(data[0], data[1], runs))
#     plt.plot(x_, np.mean(interp_client, 0), label="Client, mean: {}W, total: {}Wh".format(
#                             round(np.mean(np.mean(interp_client, 0)), 3),
#                             round(np.mean(np.mean(interp_client, 0)) * (end /3600), 3)))
#     plt.plot(x_, np.mean(interp_server, 0), label="Server, mean: {}W, total: {}Wh".format(
#                             round(np.mean(np.mean(interp_server, 0)), 3),
#                             round(np.mean(np.mean(interp_server, 0)) * (end /3600), 3)))
#     plt.legend()
#     plt.tight_layout()
#     plt.savefig("Code/Plots/Means/{}_{}.png".format(os.path.basename(__file__).partition(".py")[0], file_names))
#     return (x_, np.mean(interp_client, 0), np.mean(interp_server, 0))

# xcr, cheetah_resnet50_client, cheetah_resnet50_server = plot('Code/Plots/Results/same-device/cheetah-resnet50-50', 'cheetah-resnet50', runs=50, end=10, size=(10,4)) # 256
# xsr, SCI_HE_resnet50_client, SCI_HE_resnet50_server = plot('Code/Plots/Results/same-device/SCI_HE-resnet50-50', 'SCI_HE-resnet50', runs=50, end=10, size=(10,4)) #560
# xcs, cheetah_sqnet_client, cheetah_sqnet_server = plot('Code/Plots/Results/same-device/cheetah-sqnet-50', 'cheetah-sqnet', runs=50, end=53, size=(7,5))
# xss, SCI_HE_sqnet_client, SCI_HE_sqnet_server = plot('Code/Plots/Results/same-device/SCI_HE-sqnet-50', 'SCI_HE-sqnet', runs=50, end=82, size=(7,5))
# exit()
# # Plot means of client side
# plt.figure(figsize=(10,5))
# # plt.ylim(0, max(
# #                 max((np.max(cheetah_resnet50_client), np.max(cheetah_sqnet_client))),
# #                 # max((np.max(SCI_HE_resnet50_client), np.max(SCI_HE_sqnet_client)))))
# #                 np.max(SCI_HE_sqnet_server)))
# # plt.xlim(0, 55)
# plt.xlabel("Time (s)")
# plt.ylabel("Power consumption (W)")
# plt.title("Power usage of client while running sqnet")
# plt.plot(xcs, cheetah_sqnet_client, 
#             label="Cheetah, mean: {}W, total: {}Wh".format(
#                 round(np.mean(cheetah_sqnet_client), 1), 
#                 round(np.sum(cheetah_sqnet_client)*56/3600, 1)))
# plt.plot(xss, SCI_HE_sqnet_client, 
#             label="SCI_HE, mean: {}W, total: {}Wh".format(
#                 round(np.mean(SCI_HE_sqnet_client), 1), 
#                 round(np.sum(SCI_HE_sqnet_client)*83/3600, 1)))
# plt.legend()
# plt.savefig("Code/Plots/Means/{}_client_resnet.png".format(os.path.basename(__file__).partition(".py")[0]))

# exit()

# # Plot means of server side
# plt.figure(figsize=(10,5))
# plt.ylim(0, max(
#                 max((np.max(cheetah_resnet50_server), np.max(cheetah_sqnet_server))),
#                 # max((np.max(SCI_HE_resnet50_server), np.max(SCI_HE_sqnet_server)))))
#                 np.max(SCI_HE_sqnet_server)))
# plt.xlim(0, 55)
# plt.xlabel("Time (s)")
# plt.ylabel("Power consumption (Wh)")
# plt.title("Power usage of server")
# plt.plot(x_, cheetah_resnet50_server, label="Cheetah resnet50")
# plt.plot(x_, cheetah_sqnet_server, label="Cheetah sqnet")
# plt.plot(x_, SCI_HE_sqnet_server, label="SCI_HE resnet50")
# # plt.plot(x_, SCI_HE_resnet50_server, label="SCI_HE sqnet")
# plt.legend()
# plt.savefig("Code/Plots/Means/{}_server.png".format(os.path.basename(__file__).partition(".py")[0]))

###################### Plot first few seconds ######################

plt.figure(figsize=(11,5))
def plot(dir: str, file_names: str, runs: int, end: int, size=(int, int), shift=0, alpha=1, c1='r', c2='b'):
    """
    Plot the file in dir with name file_names

    dir         : name of the dir that the files are in
    file_names  : base of the file names
    runs        : determines how many files there are -> files go from 1 till runs+1
    end         : this script will interpolate the results from 0 till end

    returns the interpolated client and server results
    """
    x_ = np.arange(0, end, .1)
    # Open file containing all PID's and save it as string
    PID_string = open('{}/pids'.format(dir), 'r').read().split("END")
    # Convert string to python dictionary
    PID_dict = json.loads("{{{}}}".format(",".join(PID_string[:-1])))
    
    interp_client = []; interp_server = []; arr = []
    for i in range(1,runs+1):
        # Readd files and convert to numpy array
        json_string = open('{}/{}-{}.json'.format(dir, file_names, i), 'r').read().replace('\n', '')
        arr = np.array(json.loads(json_string))

        # Filter results
        start = arr[0]['host']['timestamp']
        filtered_client = filter_results(arr, PID_dict[str(i)]['client'], start=start)
        filtered_server = filter_results(arr, PID_dict[str(i)]['server'], start=start)
        
        x_y_client = np.array(list(zip(*filtered_client)))
        x_y_server = np.array(list(zip(*filtered_server)))
    
        interp_client.append(np.interp(x_, x_y_client[0], x_y_client[1], left=0, right=0))
        interp_server.append(np.interp(x_, x_y_server[0], x_y_server[1], left=0, right=0))
    
    plt.ylim(0, max(round(np.max(interp_client)), round(np.max(interp_server))*.8))
    plt.xlim(0, end)
    plt.xlabel("Time (s)")
    plt.ylabel("Power consumption (W)")
    data = file_names.split('-')
    # plt.title("Power usage of {} with {} (mean of {} runs)".format(data[0], data[1], runs))
    plt.plot(x_ + shift, np.mean(interp_client, 0), label="Client ({}, {})".format(data[0], data[1]), c=c1, alpha=alpha)
    plt.plot(x_ + shift, np.mean(interp_server, 0), label="Server ({}, {})".format(data[0], data[1]), c=c2, alpha=alpha)
    plt.legend()
    plt.tight_layout()
    # plt.savefig("Code/Plots/Means/{}_{}.png".format(os.path.basename(__file__).partition(".py")[0], file_names))
    # plt.show()
    return (x_, np.mean(interp_client, 0), np.mean(interp_server, 0))

plt.title("Power usage of both SNNIs in the first 10 seconds")
xcr, cheetah_resnet50_client, cheetah_resnet50_server = plot('Code/Plots/Results/same-device/cheetah-resnet50-50', 'cheetah-resnet50', runs=50, end=12, size=(10,4), alpha=1, c1='r', c2='b') # 256
xsr, SCI_HE_resnet50_client, SCI_HE_resnet50_server = plot('Code/Plots/Results/same-device/SCI_HE-resnet50-50', 'SCI_HE-resnet50', runs=50, end=12, size=(10,4), alpha=.5, c1='r', c2='b') #560
xcs, cheetah_sqnet_client, cheetah_sqnet_server = plot('Code/Plots/Results/same-device/cheetah-sqnet-50', 'cheetah-sqnet', runs=50, end=12, size=(7,5), shift=3.65, alpha=1, c1='g', c2='y')
xss, SCI_HE_sqnet_client, SCI_HE_sqnet_server = plot('Code/Plots/Results/same-device/SCI_HE-sqnet-50', 'SCI_HE-sqnet', runs=50, end=12, size=(7,5), shift=3.65, alpha=.5, c1='g', c2='y')

plt.text(2.2, 17.5, "Cheetah client and SCI_HE client align\n"\
                    "Cheetah server and SCI_HE server align", horizontalalignment='center')
plt.text(6.75, 15, "SCI_HE clients align, for both resnet50 and sqnet\n"\
                  "SCI_HE servers align, for both resnet50 and sqnet\n"\
                  "Cheetah clients align, for both resnet50 and sqnet\n"\
                  "Cheetah servers align, for both resnet50 and sqnet\n", horizontalalignment='center')
plt.vlines(4.4, 0, 30)
plt.tight_layout()
plt.savefig('Code/Plots/Means/mean_first10secs.png')
plt.show()
exit()



