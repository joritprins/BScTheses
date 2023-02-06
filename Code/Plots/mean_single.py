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
        if dir=='Code/Plots/Results/laptop-desktop/server-3-SCI_HE-sqnet' and i==4:
            continue
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
        print("Prepared", dir, i)

    x_ = np.arange(0, longest_run, 0.1)

    interp_client = [np.interp(x_, x_y[0], x_y[1], left=0, right=0)
                     for x_y in x_y_client]
    interp_server = [np.interp(x_, x_y[0], x_y[1], left=0, right=0)
                     for x_y in x_y_server]

    if plot == True:
        plt.figure(figsize=(10, 5))
        plt.xlabel("Time (s)")
        plt.ylabel("Power consumption (W)")
        d = dir.split('/')[-1].split('-')
        plt.title("Power usage while changing {}'s bandwith to {}Mbits with {} and {} (mean of {} runs)".format(
            d[0], d[1], d[2], d[3], runs))
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


def fastest(bw, snni, arr):
    f = min(arr, key = lambda x: x[4])
    whf = f[1] * (f[0] / 3600) + f[3] * (f[2] / 3600)
    s = max(arr, key = lambda x: x[4])
    whs = s[1] * (s[0] / 3600) + s[3] * (s[2] / 3600)
    print("{:<8} {:<10} {:<22} {:<22} {:<22} {:<22} {:<22} {:<22} {:<22} {:<22}".format(
        bw, snni, f[4], f[1], f[3], whf, s[4], s[1], s[3], whs))

def avg_time(bw, snni, arr):
    f = min(arr, key = lambda x: x[4])[4]
    s = max(arr, key = lambda x: x[4])[4]
    m = sum([i for _, _, _, _, i in arr])/len(arr)
    print("{:<12} {:<10} {:<22} {:<22} {:<22}".format(
        bw, snni, m, f, s))

def pwr(bw, snni, arr):
    pwr_c = [pwr * (time / 3600) for (time, pwr, _, _, _) in arr]
    pwr_s = [pwr * (time / 3600) for (_, _, time, pwr, _) in arr]
    pwr_t = [(pwrc * (timec / 3600)) + (pwrs * (times / 3600)) for (timec, pwrc, times, pwrs, _) in arr]

    print("{:<5} {:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
        bw, snni,
        round(min(pwr_t), 4), round(sum(pwr_t)/len(pwr_t), 4), round(max(pwr_t), 4), 
        round(min(pwr_c), 4), round(sum(pwr_c)/len(pwr_c), 4), round(max(pwr_c), 4), 
        round(min(pwr_s), 4), round(sum(pwr_s)/len(pwr_s), 4), round(max(pwr_s), 4)))
    # return min(pwr_t), sum(pwr_t)/len(pwr_t)
    return [bw, 1 if snni == 'Cheetah' else 0,
        round(min(pwr_t), 4), round(sum(pwr_t)/len(pwr_t), 4), round(max(pwr_t), 4), 
        round(min(pwr_c), 4), round(sum(pwr_c)/len(pwr_c), 4), round(max(pwr_c), 4), 
        round(min(pwr_s), 4), round(sum(pwr_s)/len(pwr_s), 4), round(max(pwr_s), 4)]


# naming = [x|c|s] [c|s] [int] [c|s][s|r]
# x = x of client and server, c = y values client, s = y values server
# c = changing max bandwith of client, s = changing max bandwith of server, b = changing bandwidth of both
# int = integer of max bandwith
# c = cheetah, s = sci_he
# r = resnet, s = sqnet50

##################################################################################################################
##################################################################################################################
##########                                                                                              ##########
##########                          CHANGING BOTH BANDWIDTH 3-30                                        ##########
##########                                                                                              ##########
##################################################################################################################
##################################################################################################################
plot = False
print("====== Changing both bandwidth ========")
# Server measurements
xb3cs,  cb3cs,  sb3cs,  db3cs  = prepare_data(dir='Code/Plots/Results/laptop-desktop/both-3-cheetah-sqnet',  runs=10, exe='sqnet-cheetah', end=0, plot=plot)
xb14cs, cb14cs, sb14cs, db14cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/both-14-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
xb30cs, cb30cs, sb30cs, db30cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/both-30-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)

xb3ss,  cb3ss,  sb3ss,  db3ss  = prepare_data(dir='Code/Plots/Results/laptop-desktop/both-3-SCI_HE-sqnet',  runs=6,  exe='sqnet-SCI_HE', end=0, plot=plot)
xb14ss, cb14ss, sb14ss, db14ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/both-14-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
xb30ss, cb30ss, sb30ss, db30ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/both-30-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)

print("Information about fastest runs with neural network sqnet")
print("{:<8} {:<10} {:<22} {:<22} {:<22} {:<22} {:<22} {:<22} {:<22} {:<22}".format(
    "Bandwith", "SNNI", "Fastest runtime (s)", "Avg power client (W)", "Avg power server (W)", "Consumed energy (Wh)", "Slowest runtime (s)", "Avg power client (W)", "Avg power server (W)", "Consumed energy (Wh)"))
fastest(3,  "Cheetah", db3cs )
fastest(14, "Cheetah", db14cs)
fastest(30, "Cheetah", db30cs)
fastest(3,  "SCI_HE",  db3ss )
fastest(14, "SCI_HE",  db14ss)
fastest(30, "SCI_HE",  db30ss)

print("More information about time with neural network sqnet")
print("{:<12} {:<10} {:<22} {:<22} {:<22}".format(
    "Bandwith", "SNNI", "Avg runtime (s)", "Min runtime (s)", "Max runtime (s)"))
avg_time(3,  "Cheetah", db3cs )
avg_time(14, "Cheetah", db14cs)
avg_time(30, "Cheetah", db30cs)
avg_time(3,  "SCI_HE",  db3ss )
avg_time(14, "SCI_HE",  db14ss)
avg_time(30, "SCI_HE",  db30ss)

tmp = []
print("Information about power with neural network sqnet")
print("{:<5} {:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
    "BW", "SNNI", 
    "Low total (Wh)",  "Avg total (Wh)",  "High total (Wh)",
    "Low client (Wh)",  "Avg client (Wh)",  "High client (Wh)",
    "Low server (Wh)",  "Avg server (Wh)",  "High server (Wh)"))
tmp.append(pwr(3,  "Cheetah", db3cs ))
tmp.append(pwr(3,  "SCI_HE",  db3ss ))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(14, "Cheetah", db14cs))
tmp.append(pwr(14, "SCI_HE",  db14ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(30, "Cheetah", db30cs))
tmp.append(pwr(30, "SCI_HE",  db30ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
print(tmp)

np.savetxt('Code/Plots/Means/both.csv', tmp, fmt='%.3f')
# exit()


##################################################################################################################
##################################################################################################################
##########                                                                                              ##########
##########                          CHANGING SERVERS AND CLIENTS BANDWIDTH 3-50                         ##########
##########                                                                                              ##########
##################################################################################################################
##################################################################################################################

print("====== Changing server's bandwidth ========")
xs3cs,  cs3cs,  ss3cs,  ds3cs  = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-3-cheetah-sqnet',  runs=10, exe='sqnet-cheetah', end=0, plot=plot)
xs14cs, cs14cs, ss14cs, ds14cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-14-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
xs30cs, cs30cs, ss30cs, ds30cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-30-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
xs50cs, cs50cs, ss50cs, ds50cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-50-cheetah-sqnet', runs=15, exe='sqnet-cheetah', end=0, plot=plot)

xs3ss,  cs3ss,  ss3ss,  ds3ss  = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-3-SCI_HE-sqnet',  runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
xs14ss, cs14ss, ss14ss, ds14ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-14-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
xs30ss, cs30ss, ss30ss, ds30ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-30-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
xs50ss, cs50ss, ss50ss, ds50ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-50-SCI_HE-sqnet', runs=15, exe='sqnet-SCI_HE', end=0, plot=plot)


xc3cs,  cc3cs,  sc3cs,  dc3cs  = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-3-cheetah-sqnet',  runs=5, exe='sqnet-cheetah', end=0, plot=plot)
xc14cs, cc14cs, sc14cs, dc14cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-14-cheetah-sqnet', runs=5, exe='sqnet-cheetah', end=0, plot=plot)
xc30cs, cc30cs, sc30cs, dc30cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-30-cheetah-sqnet', runs=5, exe='sqnet-cheetah', end=0, plot=plot)
xc50cs, cc50cs, sc50cs, dc50cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-50-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)

xc3ss,  cc3ss,  sc3ss,  dc3ss  = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-3-SCI_HE-sqnet',  runs=1, exe='sqnet-SCI_HE', end=0, plot=plot)
xc14ss, cc14ss, sc14ss, dc14ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-14-SCI_HE-sqnet', runs=5, exe='sqnet-SCI_HE', end=0, plot=plot)
xc30ss, cc30ss, sc30ss, dc30ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-30-SCI_HE-sqnet', runs=5, exe='sqnet-SCI_HE', end=0, plot=plot)
xc50ss, cc50ss, sc50ss, dc50ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-50-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)


print("Information about fastest runs with neural network sqnet")
print("{:<12} {:<10} {:<22} {:<22} {:<22} {:<18}".format(
    "Bandwith", "SNNI", "Fastest runtime (s)", "Avg power client (W)", "Avg power server (W)", "Consumed energy (Wh)"))
fastest(3,  "Cheetah", ds3cs )
fastest(14, "Cheetah", ds14cs)
fastest(30, "Cheetah", ds30cs)
fastest(50, "Cheetah", ds50cs)
fastest(3,  "SCI_HE",  ds3ss )
fastest(14, "SCI_HE",  ds14ss)
fastest(30, "SCI_HE",  ds30ss)
fastest(50, "SCI_HE",  ds50ss)

print("More information about time with neural network sqnet")
print("{:<12} {:<10} {:<22} {:<22} {:<22}".format(
    "Bandwith", "SNNI", "Avg runtime (s)", "Min runtime (s)", "Max runtime (s)"))
avg_time(3,  "Cheetah", ds3cs )
avg_time(14, "Cheetah", ds14cs)
avg_time(30, "Cheetah", ds30cs)
avg_time(50, "Cheetah", ds50cs)
avg_time(3,  "SCI_HE",  ds3ss )
avg_time(14, "SCI_HE",  ds14ss)
avg_time(30, "SCI_HE",  ds30ss)
avg_time(50, "SCI_HE",  ds50ss)

tmp = []
print("Information about power with neural network sqnet")
print("{:<5} {:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
    "BW", "SNNI", 
    "Low total (Wh)",  "Avg total (Wh)",  "High total (Wh)",
    "Low client (Wh)",  "Avg client (Wh)",  "High client (Wh)",
    "Low server (Wh)",  "Avg server (Wh)",  "High server (Wh)"))
tmp.append(pwr(3,  "Cheetah", ds3cs ))
tmp.append(pwr(3,  "SCI_HE",  ds3ss ))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(14, "Cheetah", ds14cs))
tmp.append(pwr(14, "SCI_HE",  ds14ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(30, "Cheetah", ds30cs))
tmp.append(pwr(30, "SCI_HE",  ds30ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(50, "Cheetah", ds50cs))
tmp.append(pwr(50, "SCI_HE",  ds50ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
print(tmp)

np.savetxt('Code/Plots/Means/server2.csv', tmp, fmt='%.3f')

print("====== Changing clients's bandwidth ========")
print("Information about fastest runs with neural network sqnet")
print("{:<12} {:<10} {:<22} {:<22} {:<22} {:<18}".format(
    "Bandwith", "SNNI", "Fastest runtime (s)", "Avg power client (W)", "Avg power server (W)", "Consumed energy (Wh)"))
fastest(3,  "Cheetah", dc3cs )
fastest(14, "Cheetah", dc14cs)
fastest(30, "Cheetah", dc30cs)
fastest(50, "Cheetah", dc50cs)
fastest(3,  "SCI_HE",  dc3ss )
fastest(14, "SCI_HE",  dc14ss)
fastest(30, "SCI_HE",  dc30ss)
fastest(50, "SCI_HE",  dc50ss)

print("More information about time with neural network sqnet")
print("{:<12} {:<10} {:<22} {:<22} {:<22}".format(
    "Bandwith", "SNNI", "Avg runtime (s)", "Min runtime (s)", "Max runtime (s)"))
avg_time(3,  "Cheetah", dc3cs )
avg_time(14, "Cheetah", dc14cs)
avg_time(30, "Cheetah", dc30cs)
avg_time(50, "Cheetah", dc50cs)
avg_time(3,  "SCI_HE",  dc3ss )
avg_time(14, "SCI_HE",  dc14ss)
avg_time(30, "SCI_HE",  dc30ss)
avg_time(50, "SCI_HE",  dc50ss)

tmp = []
print("Information about power with neural network sqnet")
print("{:<5} {:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
    "BW", "SNNI", 
    "Low total (Wh)",  "Avg total (Wh)",  "High total (Wh)",
    "Low client (Wh)",  "Avg client (Wh)",  "High client (Wh)",
    "Low server (Wh)",  "Avg server (Wh)",  "High server (Wh)"))
tmp.append(pwr(3,  "Cheetah", dc3cs ))
tmp.append(pwr(3,  "SCI_HE",  dc3ss ))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(14, "Cheetah", dc14cs))
tmp.append(pwr(14, "SCI_HE",  dc14ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(30, "Cheetah", dc30cs))
tmp.append(pwr(30, "SCI_HE",  dc30ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(50, "Cheetah", dc50cs))
tmp.append(pwr(50, "SCI_HE",  dc50ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
print(tmp)


np.savetxt('Code/Plots/Means/client2.csv', tmp, fmt='%.3f')


##################################################################################################################
##################################################################################################################
##########                                                                                              ##########
##########                              CHANGING SERVERS BANDWIDTH 50-500                               ##########
##########                                                                                              ##########
##################################################################################################################
##################################################################################################################
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


# tmp = [["BW", "SNNI", 
    # "Low total (Wh)",  "Avg total (Wh)",  "High total (Wh)",
    # "Low client (Wh)",  "Avg client (Wh)",  "High client (Wh)",
    # "Low server (Wh)",  "Avg server (Wh)",  "High server (Wh)"]]
tmp = []
print("Information about power with neural network sqnet")
print("{:<5} {:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
    "BW", "SNNI", 
    "Low total (Wh)",  "Avg total (Wh)",  "High total (Wh)",
    "Low client (Wh)",  "Avg client (Wh)",  "High client (Wh)",
    "Low server (Wh)",  "Avg server (Wh)",  "High server (Wh)"))
tmp.append(pwr(50,  "Cheetah", ds50cs ))
tmp.append(pwr(50,  "SCI_HE",  ds50ss ))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(100, "Cheetah", ds100cs))
tmp.append(pwr(100, "SCI_HE",  ds100ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(150, "Cheetah", ds150cs))
tmp.append(pwr(150, "SCI_HE",  ds150ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(200, "Cheetah", ds200cs))
tmp.append(pwr(200, "SCI_HE",  ds200ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(300, "Cheetah", ds300cs))
tmp.append(pwr(300, "SCI_HE",  ds300ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(400, "Cheetah", ds400cs))
tmp.append(pwr(400, "SCI_HE",  ds400ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(500, "Cheetah", ds500cs))
tmp.append(pwr(500, "SCI_HE",  ds500ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
print(tmp)

np.savetxt('Code/Plots/Means/server.csv', tmp, fmt='%.3f')

##################################################################################################################
##################################################################################################################
##########                                                                                              ##########
##########                              CHANGING CLIENTS BANDWIDTH 50-500                               ##########
##########                                                                                              ##########
##################################################################################################################
##################################################################################################################

xc50cs, cc50cs, sc50cs, dc50cs = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/client-50-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
xc100cs, cc100cs, sc100cs, dc100cs = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/client-100-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
xc150cs, cc150cs, sc150cs, dc150cs = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/client-150-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
xc200cs, cc200cs, sc200cs, dc200cs = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/client-200-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
# xc300cs, cc300cs, sc300cs, dc300cs = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/client-300-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
xc400cs, cc400cs, sc400cs, dc400cs = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/client-400-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
xc500cs, cc500cs, sc500cs, dc500cs = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/client-500-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)

xc50ss, cc50ss, sc50ss, dc50ss = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/client-50-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
xc100ss, cc100ss, sc100ss, dc100ss = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/client-100-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
xc150ss, cc150ss, sc150ss, dc150ss = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/client-150-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
xc200ss, cc200ss, sc200ss, dc200ss = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/client-200-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
# xc300ss, cc300ss, sc300ss, dc300ss = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/client-300-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
xc400ss, cc400ss, sc400ss, dc400ss = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/client-400-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
xc500ss, cc500ss, sc500ss, dc500ss = prepare_data(
    dir='Code/Plots/Results/laptop-desktop/client-500-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)

print("Information about fastest runs with neural network sqnet")
print("{:<12} {:<10} {:<22} {:<22} {:<22} {:<18}".format(
    "Bandwith", "SNNI", "Fastest runtime (s)", "Avg power client (W)", "Avg power server (W)", "Consumed energy (Wh)"))
fastest(50,  "Cheetah", dc50cs )
fastest(100, "Cheetah", dc100cs)
fastest(150, "Cheetah", dc150cs)
fastest(200, "Cheetah", dc200cs)
# fastest(300, "Cheetah", dc300cs)
fastest(400, "Cheetah", dc400cs)
fastest(500, "Cheetah", dc500cs)
fastest(50,  "SCI_HE",  dc50ss )
fastest(100, "SCI_HE",  dc100ss)
fastest(150, "SCI_HE",  dc150ss)
fastest(200, "SCI_HE",  dc200ss)
# fastest(300, "SCI_HE",  dc300ss)
fastest(400, "SCI_HE",  dc400ss)
fastest(500, "SCI_HE",  dc500ss)


print("More information about time with neural network sqnet")
print("{:<12} {:<10} {:<22} {:<22} {:<22}".format(
    "Bandwith", "SNNI", "Avg runtime (s)", "Min runtime (s)", "Max runtime (s)"))
avg_time(50,  "Cheetah", dc50cs )
avg_time(100, "Cheetah", dc100cs)
avg_time(150, "Cheetah", dc150cs)
avg_time(200, "Cheetah", dc200cs)
# avg_time(300, "Cheetah", dc300cs)
avg_time(400, "Cheetah", dc400cs)
avg_time(500, "Cheetah", dc500cs)
avg_time(50,  "SCI_HE",  dc50ss )
avg_time(100, "SCI_HE",  dc100ss)
avg_time(150, "SCI_HE",  dc150ss)
avg_time(200, "SCI_HE",  dc200ss)
# avg_time(300, "SCI_HE",  dc300ss)
avg_time(400, "SCI_HE",  dc400ss)
avg_time(500, "SCI_HE",  dc500ss)

# tmp = [ ["BW", "SNNI", 
#     "Low total (Wh)",  "Avg total (Wh)",  "High total (Wh)",
#     "Low client (Wh)",  "Avg client (Wh)",  "High client (Wh)",
#     "Low server (Wh)",  "Avg server (Wh)",  "High server (Wh)"]]
tmp = []
print("Information about power with neural network sqnet")
print("{:<5} {:<10} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
    "BW", "SNNI", 
    "Low total (Wh)",  "Avg total (Wh)",  "High total (Wh)",
    "Low client (Wh)",  "Avg client (Wh)",  "High client (Wh)",
    "Low server (Wh)",  "Avg server (Wh)",  "High server (Wh)"))
tmp.append(pwr(50,  "Cheetah", dc50cs ))
tmp.append(pwr(50,  "SCI_HE",  dc50ss ))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(100, "Cheetah", dc100cs))
tmp.append(pwr(100, "SCI_HE",  dc100ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(150, "Cheetah", dc150cs))
tmp.append(pwr(150, "SCI_HE",  dc150ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(200, "Cheetah", dc200cs))
tmp.append(pwr(200, "SCI_HE",  dc200ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
# tmp.append(# pwr(300, "Cheetah", dc300cs)
# tmp.append(# pwr(300, "SCI_HE",  dc300ss)
tmp.append(pwr(400, "Cheetah", dc400cs))
tmp.append(pwr(400, "SCI_HE",  dc400ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])
tmp.append(pwr(500, "Cheetah", dc500cs))
tmp.append(pwr(500, "SCI_HE",  dc500ss))
tmp.append([0,0,0,round(tmp[-1][3]/tmp[-2][3],2),0,0,round(tmp[-1][6]/tmp[-2][6],2),0,0,round(tmp[-1][9]/tmp[-2][9],2),0])

np.savetxt('Code/Plots/Means/client.csv', tmp, fmt='%.3f')