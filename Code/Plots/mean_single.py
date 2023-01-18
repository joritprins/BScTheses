import sys
import numpy as np
import matplotlib.pyplot as plt
import json
import os

# Insert path for functions.py file
sys.path.insert(0, '{}/..'.format(sys.path[0]))
from functions import filter_results


def read_files(dir: str, name: str, exe: str):
    json_string = open('{}/{}.json'.format(dir, name),'r').read().replace('\n', '')
    arr = np.array(json.loads(json_string))

    # Loop over results to find pid
    pid = 0
    for measurement in arr:
        for consumer in measurement['consumers']:
            if consumer['exe'] == exe:
                pid = consumer['pid']
                break  # No point in continuing
    if pid == 0:
        print("No PID found!")
        return ([], 0, 0, 0)

    start = arr[0]['host']['timestamp']
    end = arr[-1]['host']['timestamp']
    return (arr, pid, end, start)


def prepare_data(dir: str, runs: int, exe: str, end: int, plot: bool = False):
    x_y_client = []
    x_y_server = []
    data = []
    longest_run = 0

    # Loop over runs
    for i in range(1, runs+1):
        arr_client, pid_client, end_c, start_c = read_files(
            dir, 'client_{}'.format(i), exe)
        arr_server, pid_server, end_s, start_s = read_files(
            dir, 'server_{}'.format(i), exe)

        start = start_c if start_c < start_s else start_s
        end = end_c if end_c > end_s else end_s
        filtered_client = filter_results(arr_client, pid_client, start=start)
        filtered_server = filter_results(arr_server, pid_server, start=start)

        x_y_client.append(np.array(list(zip(*filtered_client))))
        x_y_server.append(np.array(list(zip(*filtered_server))))
        runtime = end-start
        if runtime > longest_run: longest_run = runtime

        data.append((end_c - start_c, np.average(x_y_client[-1][1], weights=np.diff(np.insert(x_y_client[-1][0], 0, 0))), 
                     end_s - start_s, np.average(x_y_server[-1][1], weights=np.diff(np.insert(x_y_server[-1][0], 0, 0))),
                     end - start))

    x_ = np.arange(0, longest_run, 0.1)

    interp_client = [np.interp(x_, x_y[0], x_y[1], left=0, right=0)
                     for x_y in x_y_client]
    interp_server = [np.interp(x_, x_y[0], x_y[1], left=0, right=0)
                     for x_y in x_y_server]

    if plot == True:
        plt.figure(figsize=(10, 5))
        plt.xlabel("Time (s)")
        plt.ylabel("Power consumption (W)")
        data = dir.split('/')[-1].split('-')
        plt.title("Power usage while changing {}'s bandwith to {}Mbits with {} and {} (mean of {} runs)".format(
            data[0], data[1], data[2], data[3], runs))
        plt.plot(x_, np.mean(interp_client, 0), label="Client, mean: {}W, total: {}Wh".format(
            round(np.mean(np.mean(interp_client, 0)), 3),
            round(np.mean(np.mean(interp_client, 0)) * (longest_run / 3600), 3)))
        plt.plot(x_, np.mean(interp_server, 0), label="Server, mean: {}W, total: {}Wh".format(
            round(np.mean(np.mean(interp_server, 0)), 3),
            round(np.mean(np.mean(interp_server, 0)) * (longest_run / 3600), 3)))
        plt.ylim(bottom=0)
        plt.xlim(-3, longest_run + 3)
        plt.legend()
        plt.savefig("Code/Plots/Means/{}_{}.png".format(
            os.path.basename(__file__).partition(".py")[0], dir.split('/')[-1]))
    return (x_, np.mean(interp_client, 0), np.mean(interp_server, 0), data)


# naming = [x|c|s] [c|s] [int] [c|s][s|r]
# x = x of client and server, c = y values client, s = y values server
# c = changing max bandwith of client, s = changing max bandwith of server
# int = integer of max bandwith
# c = cheetah, s = sci_he
# r = resnet, s = sqnet50
plot = False
xs50cs, cs50cs, ss50cs, ds50cs = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/server-50-cheetah-sqnet', runs=15, exe='sqnet-cheetah', end=0, plot=plot)
xs100cs, cs100cs, ss100cs, ds100cs = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/server-100-cheetah-sqnet', runs=15, exe='sqnet-cheetah', end=0, plot=plot)
xs150cs, cs150cs, ss150cs, ds150cs = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/server-150-cheetah-sqnet', runs=15, exe='sqnet-cheetah', end=0, plot=plot)
xs200cs, cs200cs, ss200cs, ds200cs = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/server-200-cheetah-sqnet', runs=15, exe='sqnet-cheetah', end=0, plot=plot)
xs300cs, cs300cs, ss300cs, ds300cs = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/server-300-cheetah-sqnet', runs=15, exe='sqnet-cheetah', end=0, plot=plot)
xs400cs, cs400cs, ss400cs, ds400cs = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/server-400-cheetah-sqnet', runs=15, exe='sqnet-cheetah', end=0, plot=plot)
xs500cs, cs500cs, ss500cs, ds500cs = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/server-500-cheetah-sqnet', runs=15, exe='sqnet-cheetah', end=0, plot=plot)

xs50ss, cs50ss, ss50ss, ds50ss = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/server-50-SCI_HE-sqnet', runs=15, exe='sqnet-SCI_HE', end=0, plot=plot)
xs100ss, cs100ss, ss100ss, ds100ss = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/server-100-SCI_HE-sqnet', runs=15, exe='sqnet-SCI_HE', end=0, plot=plot)
xs150ss, cs150ss, ss150ss, ds150ss = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/server-150-SCI_HE-sqnet', runs=15, exe='sqnet-SCI_HE', end=0, plot=plot)
xs200ss, cs200ss, ss200ss, ds200ss = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/server-200-SCI_HE-sqnet', runs=15, exe='sqnet-SCI_HE', end=0, plot=plot)
xs300ss, cs300ss, ss300ss, ds300ss = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/server-300-SCI_HE-sqnet', runs=15, exe='sqnet-SCI_HE', end=0, plot=plot)
xs400ss, cs400ss, ss400ss, ds400ss = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/server-400-SCI_HE-sqnet', runs=15, exe='sqnet-SCI_HE', end=0, plot=plot)
xs500ss, cs500ss, ss500ss, ds500ss = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/server-500-SCI_HE-sqnet', runs=15, exe='sqnet-SCI_HE', end=0, plot=plot)


def f_(arr):
    f = min(arr, key = lambda x: x[4])
    wh = f[1] * (f[0] / 3600) + f[3] * (f[2] / 3600)
    return (f[4], f[1], f[3], wh)
def fastest(bw, snni, arr):
    f = f_(arr)
    print("{:<12} {:<10} {:<22} {:<22} {:<22} {:<18}".format(
        bw, snni, f[0], f[1], f[2], f[3]))

print("Information about fastest runs with neural network sqnet")
print("{:<12} {:<10} {:<22} {:<22} {:<22} {:<18}".format(
    "Bandwith", "SNNI", "Fastest runtime (s)", "Avg power client (W)", "Avg power server (W)", "Consumed energy (Wh)"))
fastest(50,  "Cheetah", ds50cs )
fastest(100, "Cheetah", ds100cs)
fastest(150, "Cheetah", ds150cs)
fastest(200, "Cheetah", ds200cs)
fastest(300, "Cheetah", ds300cs)
fastest(400, "Cheetah", ds400cs)
fastest(500, "Cheetah", ds500cs)
fastest(50,  "SCI_HE",  ds50ss )
fastest(100, "SCI_HE",  ds100ss)
fastest(150, "SCI_HE",  ds150ss)
fastest(200, "SCI_HE",  ds200ss)
fastest(300, "SCI_HE",  ds300ss)
fastest(400, "SCI_HE",  ds400ss)
fastest(500, "SCI_HE",  ds500ss)


def d_(arr):
    f = min(arr, key = lambda x: x[4])[4]
    s = max(arr, key = lambda x: x[4])[4]
    m = sum([i for _, _, _, _, i in arr])/len(arr)
    return (m, f, s)
def avg_time(bw, snni, arr):
    d = d_(arr)
    print("{:<12} {:<10} {:<22} {:<22} {:<22}".format(
        bw, snni, d[0], d[1], d[2]))

print("More information about time with neural network sqnet")
print("{:<12} {:<10} {:<22} {:<22} {:<22}".format(
    "Bandwith", "SNNI", "Avg runtime (s)", "Min runtime (s)", "Max runtime (s)"))
avg_time(50,  "Cheetah", ds50cs )
avg_time(100, "Cheetah", ds100cs)
avg_time(150, "Cheetah", ds150cs)
avg_time(200, "Cheetah", ds200cs)
avg_time(300, "Cheetah", ds300cs)
avg_time(400, "Cheetah", ds400cs)
avg_time(500, "Cheetah", ds500cs)
avg_time(50,  "SCI_HE",  ds50ss )
avg_time(100, "SCI_HE",  ds100ss)
avg_time(150, "SCI_HE",  ds150ss)
avg_time(200, "SCI_HE",  ds200ss)
avg_time(300, "SCI_HE",  ds300ss)
avg_time(400, "SCI_HE",  ds400ss)
avg_time(500, "SCI_HE",  ds500ss)

def pwr(bw, snni, arr):
    d = d_(arr)
    print("{:<12} {:<10} {:<22} {:<22} {:<22}".format(
        bw, snni, d[0], d[1], d[2]))

print("Information about power with neural network sqnet")
print("{:<12} {:<10} {:<22} {:<22} {:<22}".format(
    "Bandwith", "SNNI", "Avg runtime (s)", "Min runtime (s)", "Max runtime (s)"))
avg_time(50,  "Cheetah", ds50cs )
avg_time(100, "Cheetah", ds100cs)
avg_time(150, "Cheetah", ds150cs)
avg_time(200, "Cheetah", ds200cs)
avg_time(300, "Cheetah", ds300cs)
avg_time(400, "Cheetah", ds400cs)
avg_time(500, "Cheetah", ds500cs)
avg_time(50,  "SCI_HE",  ds50ss )
avg_time(100, "SCI_HE",  ds100ss)
avg_time(150, "SCI_HE",  ds150ss)
avg_time(200, "SCI_HE",  ds200ss)
avg_time(300, "SCI_HE",  ds300ss)
avg_time(400, "SCI_HE",  ds400ss)
avg_time(500, "SCI_HE",  ds500ss)
