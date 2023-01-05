# Insert path for functions.py file
import sys
sys.path.insert(0, '{}/..'.format(sys.path[0]))

import numpy as np
import matplotlib.pyplot as plt
import json

json_string = open('Code/_log.json', 'r').read().replace('\n', '')
arr = np.array(json.loads(json_string))

start = arr[0]['host']['timestamp']
client_pid = 61937
server_pid = 61939

from functions import filter_results
from functions import wh_to_w

filtered_client = filter_results(arr, client_pid)
filtered_server = filter_results(arr, server_pid)

x_y_client = np.array(list(zip(*filtered_client)))
x_y_server = np.array(list(zip(*filtered_server)))

plt.plot(x_y_client[0],x_y_client[1], label="client")
plt.plot(x_y_server[0],x_y_server[1], label="server")
plt.legend()
plt.show()



wattsc = np.array(list(zip(*wh_to_w(filtered_client))))
plt.figure(figsize=(10,5))
plt.plot(wattsc[0],wattsc[1], color='red', label="Power usage client in terms of W")
plt.plot(x_y_client[0],x_y_client[1], color='blue', label="Power usage client in terms of Wh")
plt.xlabel("Time (s)")
plt.ylabel("Power")
plt.title("Power consumption")
plt.legend()
# plt.savefig("Code/Results/{}".format(args.name))
plt.show()
exit()

wattss = np.array(list(zip(*wh_to_w(filtered_server))))
# plt.figure(figsize=(10,5))
# plt.plot(wattss[0],wattss[1], color='red', label="Power usage client in terms of W")
# plt.plot(x_y_server[0],x_y_server[1], color='blue', label="Power usage client in terms of Wh")
# plt.xlabel("Time (s)")
# plt.ylabel("Power")
# plt.title("Power consumption")
# plt.legend()
# # plt.savefig("Code/Results/{}".format(args.name))
# plt.show()

plt.xlabel("Time (s)")
plt.ylabel("Power")
plt.plot(wattss[0],wattss[1], color='red', label="Power usage client in terms of W")
plt.plot(x_y_server[0],x_y_server[1], color='blue', label="Power usage client in terms of Wh")
plt.plot(wattsc[0],wattsc[1], color='green', label="Power usage client in terms of W")
plt.plot(x_y_client[0],x_y_client[1], color='orange', label="Power usage client in terms of Wh")
plt.title("Power consumption")
plt.legend()
plt.show()


# plt.figure(figsize=(10,5))
# plt.plot(x_y[0], x_y[1], label="Scaphandre")
# plt.ylim(0, 100)
# plt.xlim(0, np.max(x_y[0]))
# plt.xlabel("Time (s)")
# plt.ylabel("Percentage of CPU (%)")
# plt.title("CPU usage of Scaphandre")
# plt.legend()
# plt.savefig("Code/Plots/{}.png".format(os.path.basename(__file__).partition(".py")[0]))
# plt.show()