import numpy as np
import matplotlib.pyplot as plt
import json
import datetime
import argparse
parser = argparse.ArgumentParser()

default_client = open('Cheetah/data/client', 'r').read()
default_server = open('Cheetah/data/server', 'r').read()

parser.add_argument("-c", "--client_pid", help="PID of the client process", type=int, default=default_client)
parser.add_argument("-s", "--server_pid", help="PID of the server process", type=int, default=default_server)
parser.add_argument("-f", "--file", help="JSON file to read the data from", default='Code/log.json')
parser.add_argument("-n", "--name", help="Name for the plot", default='Power usage')
args = parser.parse_args()

print("Running parser on file: {} with server_pid: {} and client_pid: {}".format(args.file, args.server_pid, args.client_pid))

json_string = open(args.file, 'r').read().replace('\n', '')
arr = np.array(json.loads(json_string))

start = arr[0]['host']['timestamp']
filtered_client = [
    (round(consumer['timestamp']-start, 3), consumer['consumption']/1000000) 
        for measurement in arr 
            for consumer in measurement['consumers'] 
                if consumer['pid'] == args.client_pid]
filtered_server = [
    (round(consumer['timestamp']-start, 3), consumer['consumption']/1000000) 
        for measurement in arr 
            for consumer in measurement['consumers'] 
                if consumer['pid'] == args.server_pid]

x_y_client = np.array(list(zip(*filtered_client)))
x_y_server = np.array(list(zip(*filtered_server)))


plt.figure(figsize=(10,10))
plt.plot(x_y_client[0],x_y_client[1], label="Client (mean: {}W".format(round(np.mean(x_y_client[1]), 2)))
plt.plot(x_y_server[0],x_y_server[1], label="Server (mean: {}W".format(round(np.mean(x_y_server[1]), 2)), c='r')
plt.scatter(x_y_client[0],x_y_client[1])
plt.scatter(x_y_server[0],x_y_server[1], c='r')
plt.ylim(0, max(np.max(x_y_client[1]), np.max(x_y_server[1])))
plt.xlabel("Time (s)")
plt.ylabel("Power (W)")
plt.title("Power consumption")
plt.legend()
plt.savefig(args.name)
# plt.show()





# [consumer for consumer in measurement['consumers'] for measurement in np_arr if consumer['pid'] ]
# for measurement in np_arr:
#     for consumer in measurement['consumers']:
#         print(consumer)
# print(filtered)
# start = filtered[0]['timestamp']
# print(datetime.time(start))
# for time in filtered:
    # print(datetime.time.fromtimestamp(time['timestamp'] - start))
# 32587
# f = open("Code/log.json", 'r')
# for line in f:
    # print(line, "\n\n\n")
# arr = np.array(f.read())[1:-1]
# print(arr)

