import numpy as np
import matplotlib.pyplot as plt
import json
import argparse
parser = argparse.ArgumentParser()

# default_client = open('Cheetah/data/client', 'r').read()
# default_server = open('Cheetah/data/server', 'r').read()
default_client=1
default_server=1

# parser.add_argument("-c", "--client_pid", help="PID of the client process", type=int, default=default_client)
# parser.add_argument("-s", "--server_pid", help="PID of the server process", type=int, default=default_server)
# parser.add_argument("-f", "--file", help="JSON file to read the data from", default='Code/log.json')
# parser.add_argument("-o", "--output_file", help="File to write the raw data in", default='output')
# parser.add_argument("-n", "--name", help="Name for the plot", default='Power usage')
# args = parser.parse_args()
scaphandrepid = 30242
serverpid = 30262
clientpid = 30259

# print("Running parser on file: {} with server_pid: {} and client_pid: {}".format(args.file, args.server_pid, args.client_pid))
# print("Command to run: sudo python3 Code/parse_results.py -c {} -s {} -f {} -o {} -n {}".format(args.client_pid, args.server_pid, args.file, args.output_file, args.name))

json_string = open("_log.json", 'r').read().replace('\n', '')
arr = np.array(json.loads(json_string))

start = arr[0]['host']['timestamp']
filtered_client = [
    (round(consumer['timestamp']-start, 3), consumer['consumption']/1000000) 
        for measurement in arr 
            for consumer in measurement['consumers'] 
                if consumer['pid'] == serverpid]
filtered_server = [
    (round(consumer['timestamp']-start, 3), consumer['consumption']/1000000) 
        for measurement in arr 
            for consumer in measurement['consumers'] 
                if consumer['pid'] == clientpid]
filtered_scaphandre = [
    (round(consumer['timestamp']-start, 3), consumer['consumption']/1000000) 
        for measurement in arr 
            for consumer in measurement['consumers'] 
                if consumer['pid'] == scaphandrepid]

print(len(filtered_client), len(filtered_server), len(filtered_scaphandre))

x_y_client = np.array(list(zip(*filtered_client)))
x_y_server = np.array(list(zip(*filtered_server)))
x_y_scaphandre = np.array(list(zip(*filtered_scaphandre)))

if False: # For printing time differences
    print(x_y_client)
    difference = [x - x_y_client[i-1] for i, x in enumerate(x_y_client) if i>0]
    print(difference)
    
    filtered_client = [
        (round(consumer['timestamp']-start, 3), consumer['consumption']/1000000) 
            for measurement in arr 
                for consumer in measurement['consumers'] 
                    if consumer['pid'] == args.client_pid]
    
    print(filtered_client)
    print("------------------")
    for i, x in enumerate(filtered_client):
        if i>0:
            print(x[0]-filtered_client[i-1][0])
    # print(difference)
if True:
    plt.figure(figsize=(10,10))
    plt.plot(x_y_client[0],x_y_client[1], label="Client (mean: {}W".format(round(np.mean(x_y_client[1]), 2)))
    plt.plot(x_y_server[0],x_y_server[1], label="Server (mean: {}W".format(round(np.mean(x_y_server[1]), 2)), c='r')
    plt.plot(x_y_scaphandre[0],x_y_scaphandre[1], label="Scaphandre (mean: {}W".format(round(np.mean(x_y_scaphandre[1]), 2)), c='g')
    plt.scatter(x_y_client[0],x_y_client[1])
    plt.scatter(x_y_server[0],x_y_server[1], c='r')
    plt.scatter(x_y_scaphandre[0],x_y_scaphandre[1], c='g')
    plt.ylim(0, max(np.max(x_y_client[1]), np.max(x_y_server[1])))
    plt.xlabel("Time (s)")
    plt.ylabel("Power (W)")
    plt.title("Power consumption")
    plt.legend()
    # plt.savefig("Code/Results/{}".format(args.name))
    plt.show()

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

if False:
    client_log =  open("Cheetah/cheetah-sqnet_client.log", 'r')
    # for line in client_log:
    #     if line.startswith("~"):
    #         print(line, end="")
    # client_log_filtered = [line for line in client_log if line.startswith("~")]
    client_log_filtered = [line.replace('\n','').replace('~ ', '').split(' ') for line in client_log if line.startswith("~")]
    # client_log_filtered = [s.replace('\n', '') for s in client_log_filtered]
    print(client_log_filtered)
    # print(log)
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
    # plt.savefig("Code/Results/{}_test.png".format(args.name))
    plt.show()


# print(x_y_client)
# f1 = open("Code/Results/client_{}".format(args.output_file), 'ab')
# np.savetxt(f1, x_y_client)
# # np.savetxt(f1, x_y_client[1])
# f2 = open("Code/Results/server_{}".format(args.output_file), 'ab')
# np.savetxt(f2, x_y_server)
# # np.savetxt(f2, x_y_server[1])
