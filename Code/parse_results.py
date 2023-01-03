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

json_string = open(args.file, 'r').read().replace('\n', '')
arr = np.array(json.loads(json_string))

start = arr[0]['host']['timestamp']


def filter_results(arr, pid: int):
    """
    Function that filters the data from one process from an array of power measurements
    
    @arr: array containing power measurements 
    @pid: pid of the process that needs to be filtered out
    """
    return [
        (round(consumer['timestamp']-start, 3), consumer['consumption']/1000000) 
            for measurement in arr 
                for consumer in measurement['consumers'] 
                    if consumer['pid'] == pid]

filtered_client = filter_results(arr, args.client_pid)
filtered_server = filter_results(arr, args.server_pid)

x_y_client = np.array(list(zip(*filtered_client)))
x_y_server = np.array(list(zip(*filtered_server)))

def aggregate_results(arr, step):
    """
    Aggregates the results
    
    arr : 2d array containing timestamps and given wattages: [[t0, t1, ..., tn][w0, w1, ..., wn]]
    step: step of returning array
    
    returns array in the form of [[0, 1*step, ..., m*step][w0^, w1^, ...,, wm^]] 
        where m*step < tn
    """
    last_time, last_pwr, i = arr[0][0], arr[0][1], 0 
    pwr1 = (  (step*last_pwr) / last_time  )
    
    x_y_aggr = []
    
    print(x_y_client[0][-1])
    
    for t in np.arange(0, x_y_client[0][-1], step):
        if t > arr[i][0]:
            new_time, new_pwr = arr[i+1][0] - arr[i][0], arr[i+1][1]
            pwr2 = (  (step*new_pwr) / (new_time)  )
    
            frac = ( t - arr[i][0] ) / step
            x_y_aggr.append(  (t, frac * new_pwr + (1-frac) * last_pwr)   )
    
            i+=1
            last_time, last_pwr, pwr1 = new_time, new_pwr, pwr2
        else:
            x_y_aggr.append(  (t, pwr1)  )
    
    return np.array(list(zip(*x_y_aggr)))

# Print client beside of server in scatter and plot
if False:
    plt.figure(figsize=(20,10))
    plt.plot(x_y_client[0],x_y_client[1], label="Client (mean: {}W".format(round(np.mean(x_y_client[1]), 2)))
    plt.plot(x_y_server[0],x_y_server[1], label="Server (mean: {}W".format(round(np.mean(x_y_server[1]), 2)), c='r')
    plt.scatter(x_y_client[0],x_y_client[1])
    plt.scatter(x_y_server[0],x_y_server[1], c='r')
    plt.ylim(0, max(np.max(x_y_client[1]), np.max(x_y_server[1])))
    plt.xlabel("Time (s)")
    plt.ylabel("Power (W)")
    plt.title("Power consumption")
    plt.legend()
    # plt.savefig("Code/Results/{}".format(args.name))
    plt.show()

# Print client beside of server in bar
if True:
    plt.figure(figsize=(20,10))
    print(x_y_client[0])
    print(np.diff(x_y_client[0]))
    plt.bar(x_y_client[0][1:], height=x_y_client[1][1:], width=np.diff(x_y_client[0]) * -1, align='edge', edgecolor='black')
    # plt.plot(x_y_client[0],x_y_client[1], label="Client (mean: {}W".format(round(np.mean(x_y_client[1]), 2)))
    # plt.plot(x_y_server[0],x_y_server[1], label="Server (mean: {}W".format(round(np.mean(x_y_server[1]), 2)), c='r')
    plt.scatter(x_y_client[0],x_y_client[1])
    # plt.scatter(x_y_server[0],x_y_server[1], c='r')
    # plt.ylim(0, max(np.max(x_y_client[1]), np.max(x_y_server[1])))
    plt.xlabel("Time (s)")
    plt.ylabel("Power (W)")
    plt.title("Power consumption")
    plt.legend()
    # plt.savefig("Code/Results/{}".format(args.name))
    plt.show()

# Print aggregated with normal
if False:
    x_y_client_aggr = aggregate_results(filtered_client, 0.1)
    plt.figure(figsize=(20,10))
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
    plt.ylabel("Power (W)")
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
