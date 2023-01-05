import numpy as np
import matplotlib.pyplot as plt
import json
import argparse
parser = argparse.ArgumentParser()

default_client = open('Cheetah/data/client', 'r').read()
default_server = open('Cheetah/data/server', 'r').read()

parser.add_argument("-c", "--client_pid", help="PID of the client process", type=int, default=default_client)
parser.add_argument("-s", "--server_pid", help="PID of the server process", type=int, default=default_server)
parser.add_argument("-f", "--file", help="JSON file to read the data from", default='Code/log.json')
parser.add_argument("-o", "--output_file", help="File to write the raw data in", default='output')
parser.add_argument("-n", "--name", help="Name for the plot", default='Power usage')
args = parser.parse_args()

print("Running parser on file: {} with server_pid: {} and client_pid: {}".format(args.file, args.server_pid, args.client_pid))
print("Command to run: sudo python3 Code/parse_results.py -c {} -s {} -f {} -o {} -n {}".format(args.client_pid, args.server_pid, args.file, args.output_file, args.name))

# Open file containing power consumption information and convert to array
json_string = open(args.file, 'r').read().replace('\n', '')
arr = np.array(json.loads(json_string))

start = arr[0]['host']['timestamp']

from functions import filter_results 
filtered_client = filter_results(arr, args.client_pid, start=start)
filtered_server = filter_results(arr, args.server_pid, start=start)

x_y_client = np.array(list(zip(*filtered_client)))
x_y_server = np.array(list(zip(*filtered_server)))

# Print client beside of server in scatter and plot
if False:
    plt.figure(figsize=(10,5))
    plt.plot(x_y_client[0],x_y_client[1], label="Client (mean: {}W".format(round(np.mean(x_y_client[1]), 2)))
    plt.plot(x_y_server[0],x_y_server[1], label="Server (mean: {}W".format(round(np.mean(x_y_server[1]), 2)), c='r')
    plt.scatter(x_y_client[0],x_y_client[1])
    plt.scatter(x_y_server[0],x_y_server[1], c='r')
    plt.ylim(0, max(np.max(x_y_client[1]), np.max(x_y_server[1])))
    plt.xlabel("Time (s)")
    plt.ylabel("Power (Wh)")
    plt.title("Power consumption")
    plt.legend()
    # plt.savefig("Code/Results/{}".format(args.name))
    plt.show()

# Print client beside of server in bar
if False:
    plt.figure(figsize=(10,5))
    print(x_y_client[0])
    print(np.diff(x_y_client[0]))
    plt.bar(x_y_client[0][1:], height=x_y_client[1][1:], width=np.diff(x_y_client[0]) * -1, align='edge', edgecolor='black')
    # plt.plot(x_y_client[0],x_y_client[1], label="Client (mean: {}W".format(round(np.mean(x_y_client[1]), 2)))
    # plt.plot(x_y_server[0],x_y_server[1], label="Server (mean: {}W".format(round(np.mean(x_y_server[1]), 2)), c='r')
    plt.scatter(x_y_client[0],x_y_client[1])
    # plt.scatter(x_y_server[0],x_y_server[1], c='r')
    # plt.ylim(0, max(np.max(x_y_client[1]), np.max(x_y_server[1])))
    plt.xlabel("Time (s)")
    plt.ylabel("Power (Wh)")
    plt.title("Power consumption")
    plt.legend()
    # plt.savefig("Code/Results/{}".format(args.name))
    plt.show()

if True:
    from functions import wh_to_w
    watts = np.array(list(zip(*wh_to_w(filtered_client))))
    plt.figure(figsize=(10,5))
    plt.plot(watts[0],watts[1], color='red', label="Power usage client in terms of W")
    plt.plot(x_y_client[0],x_y_client[1], color='blue', label="Power usage client in terms of Wh")
    plt.xlabel("Time (s)")
    plt.ylabel("Power")
    plt.title("Power consumption")
    plt.legend()
    # plt.savefig("Code/Results/{}".format(args.name))
    plt.show()

    watts = np.array(list(zip(*wh_to_w(filtered_client))))
    plt.figure(figsize=(10,5))
    plt.plot(watts[0],watts[1], color='red', label="Power usage client in terms of W")
    plt.plot(x_y_client[0],x_y_client[1], color='blue', label="Power usage client in terms of Wh")
    plt.xlabel("Time (s)")
    plt.ylabel("Power")
    plt.title("Power consumption")
    plt.legend()
    # plt.savefig("Code/Results/{}".format(args.name))
    plt.show()

# Print aggregated with normal
if False:
    x_y_client_aggr = aggregate_results(filtered_client, 0.1)
    plt.figure(figsize=(10,5))
    plt.plot(x_y_client[0], x_y_client[1], label="client")
    plt.scatter(x_y_client_aggr[0], x_y_client_aggr[1], label="aggr", c='red')
    plt.plot(x_y_client_aggr[0], x_y_client_aggr[1], label="aggr", c='red')
    plt.show()

# Aggregate results with savgol_filter
if False:
    from scipy.signal import savgol_filter
    yhat_client = savgol_filter(x_y_client[1], 10, 3)
    yhat_server = savgol_filter(x_y_server[1], 10, 3)
    plt.figure(figsize=(10,10))
    plt.plot(x_y_client[0],yhat_client, label="Client (mean: {}W".format(round(np.mean(yhat_client), 2)))
    plt.plot(x_y_server[0],yhat_server, label="Server (mean: {}W".format(round(np.mean(yhat_server), 2)), c='r')
    plt.scatter(x_y_client[0],x_y_client[1])
    plt.scatter(x_y_server[0],x_y_server[1], c='r')
    plt.ylim(0, max(np.max(x_y_client[1]), np.max(x_y_server[1])))
    plt.xlabel("Time (s)")
    plt.ylabel("Power (Wh)")
    plt.title("Power consumption flattened")
    plt.legend()
    plt.savefig("Code/Results/{}_flattened.png".format(args.name))
    plt.show()

# Tests with logs
if False:
    client_log =  open("Cheetah/cheetah-sqnet_client.log", 'r')
    for line in client_log:
        if line.startswith("~"):
            print(line, end="")
    client_log_filtered = [line for line in client_log if line.startswith("~")]
    client_log_filtered = [line.replace('\n','').replace('~ ', '').split(' ') for line in client_log if line.startswith("~")]
    client_log_filtered = [s.replace('\n', '') for s in client_log_filtered]
    print(client_log_filtered)
    print(log)
