"""
Prints the overhead caused by scaphandre of one run
"""
__author__ = "Jorit Prins"

# Insert path for functions.py file
import sys
sys.path.insert(0, '{}/..'.format(sys.path[0]))
sys.path.insert(0, '{}/../..'.format(sys.path[0]))

import numpy as np
import matplotlib.pyplot as plt
import json
import os
from functions import filter_results

avg = False
all = False
total = False
med = False
test = True

total_nr = 0
def read_files(dir: str, name: str, exe: str):
    """
    Read files

    dir         : name of the dir that the files are in
    name        : base of the file names
    exe         : name of process to filter

    returns array containing data, pid of process, end of measurements 
    and start of measurements
    """
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


def prepare_data(dir: str, runs: int, exe: str, end: int):
    """
    Read files and prepare data

    dir         : name of the dir that the files are in
    exe         : base of the file names
    runs        : determines how many files there are -> files go from 1 till runs+1
    end         : this script will interpolate the results from 0 till end
    plot        : if true, plot the results

    returns the interpolated client and server results
    """
    global total_nr
    # if not total:
        # print(dir)
    times = []
    # Loop over runs
    if test:
        print(dir)
    for i in range(1, runs+1):
        if dir=='Code/Plots/Results/laptop-desktop/server-3-SCI_HE-sqnet' and i==4:
            continue
        if dir=='Code/Plots/Results/laptop-desktop/both-30-cheetah-sqnet' and i==6:
            continue

        if dir=='Code/Plots/Results/laptop-desktop/both-3-cheetah-sqnet' and i==8:
            continue
        if dir=='Code/Plots/Results/laptop-desktop/both-3-cheetah-sqnet' and i==9:
            continue
        if dir=='Code/Plots/Results/laptop-desktop/both-3-SCI_HE-sqnet' and i==2:
            continue
        if dir=='Code/Plots/Results/laptop-desktop/both-3-SCI_HE-sqnet' and i==5:
            continue
        if dir=='Code/Plots/Results/laptop-desktop/both-3-SCI_HE-sqnet' and i==6:
            continue
        if dir=='Code/Plots/Results/laptop-desktop/both-14-SCI_HE-sqnet' and i==4:
            continue
        arr_client, pid_client, end_c, start_c = read_files(
            dir, 'client_{}'.format(i), exe)
        arr_server, pid_server, end_s, start_s = read_files(
            dir, 'server_{}'.format(i), exe)

        start = start_c if start_c < start_s else start_s
        end = end_c if end_c > end_s else end_s
        if all:
            print(i, end-start)
        if total:
            total_nr += end-start
        else: 
            total_nr = 0
        times.append(end-start)
        if test:
            print(i, end-start, "[", (end_c - start_c)-(end_s - start_s) ,"]", "(", end_c - start_c, ")", "(", end_s - start_s, ")")
            # if (end_c - start_c)-(end_s - start_s) > 10 or (end_c - start_c)-(end_s - start_s) < -10:
                # print(i, (end_c - start_c)-(end_s - start_s))
    if avg:
        print(np.mean(times), end=",")
    if med:
        print(np.median(times), end=',')
        
    return 0,0,0,0

plot=False

# xc50cs, cc50cs, sc50cs, dc50cs = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/client-50-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
# xc100cs, cc100cs, sc100cs, dc100cs = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/client-100-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
# xc150cs, cc150cs, sc150cs, dc150cs = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/client-150-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
# xc200cs, cc200cs, sc200cs, dc200cs = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/client-200-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)

# xc50ss, cc50ss, sc50ss, dc50ss = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/client-50-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
# xc100ss, cc100ss, sc100ss, dc100ss = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/client-100-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
# xc150ss, cc150ss, sc150ss, dc150ss = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/client-150-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
# xc200ss, cc200ss, sc200ss, dc200ss = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/client-200-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)

# xs50cs, cs50cs, ss50cs, ds50cs = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/server-50-cheetah-sqnet', runs=15, exe='sqnet-cheetah', end=0, plot=plot)
# xs100cs, cs100cs, ss100cs, ds100cs = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/server-100-cheetah-sqnet', runs=15, exe='sqnet-cheetah', end=0, plot=plot)
# xs150cs, cs150cs, ss150cs, ds150cs = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/server-150-cheetah-sqnet', runs=15, exe='sqnet-cheetah', end=0, plot=plot)
# xs200cs, cs200cs, ss200cs, ds200cs = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/server-200-cheetah-sqnet', runs=15, exe='sqnet-cheetah', end=0, plot=plot)

# xs50ss, cs50ss, ss50ss, ds50ss = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/server-50-SCI_HE-sqnet', runs=15, exe='sqnet-SCI_HE', end=0, plot=plot)
# xs100ss, cs100ss, ss100ss, ds100ss = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/server-100-SCI_HE-sqnet', runs=15, exe='sqnet-SCI_HE', end=0, plot=plot)
# xs150ss, cs150ss, ss150ss, ds150ss = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/server-150-SCI_HE-sqnet', runs=15, exe='sqnet-SCI_HE', end=0, plot=plot)
# xc200ss, cc200ss, sc200ss, dc200ss = prepare_data(
#     dir='Code/Plots/Results/laptop-desktop/client-200-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)


print("both 3-30")# sqnet both 3-30
xb3cs,  cb3cs,  sb3cs,  db3cs  = prepare_data(dir='Code/Plots/Results/laptop-desktop/both-3-cheetah-sqnet',  runs=10, exe='sqnet-cheetah', end=0, plot=plot)
xb14cs, cb14cs, sb14cs, db14cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/both-14-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
xb30cs, cb30cs, sb30cs, db30cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/both-30-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
print()
xb3ss,  cb3ss,  sb3ss,  db3ss  = prepare_data(dir='Code/Plots/Results/laptop-desktop/both-3-SCI_HE-sqnet',  runs=6,  exe='sqnet-SCI_HE', end=0, plot=plot)
xb14ss, cb14ss, sb14ss, db14ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/both-14-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
xb30ss, cb30ss, sb30ss, db30ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/both-30-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
print("{}hr {}mins ({}s)".format(round(total_nr/60/60), total_nr%(60*60), round(total_nr, 5)))
total_nr=0
print("server 3-50")# sqnet server 3-50
xs3cs,  cs3cs,  ss3cs,  ds3cs  = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-3-cheetah-sqnet',  runs=10, exe='sqnet-cheetah', end=0, plot=plot)
xs14cs, cs14cs, ss14cs, ds14cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-14-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
xs30cs, cs30cs, ss30cs, ds30cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-30-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
xs50cs, cs50cs, ss50cs, ds50cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-50-cheetah-sqnet', runs=15, exe='sqnet-cheetah', end=0, plot=plot)
print()

xs3ss,  cs3ss,  ss3ss,  ds3ss  = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-3-SCI_HE-sqnet',  runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
xs14ss, cs14ss, ss14ss, ds14ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-14-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
xs30ss, cs30ss, ss30ss, ds30ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-30-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
xs50ss, cs50ss, ss50ss, ds50ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/server-50-SCI_HE-sqnet', runs=15, exe='sqnet-SCI_HE', end=0, plot=plot)
print("{}hr {}mins ({}s)".format(round(total_nr/60/60), total_nr%(60*60), round(total_nr, 5)))
total_nr=0

print("client 3-50")# sqnet client 3-50
xc3cs,  cc3cs,  sc3cs,  dc3cs  = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-3-cheetah-sqnet',  runs=5, exe='sqnet-cheetah', end=0, plot=plot)
xc14cs, cc14cs, sc14cs, dc14cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-14-cheetah-sqnet', runs=5, exe='sqnet-cheetah', end=0, plot=plot)
xc30cs, cc30cs, sc30cs, dc30cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-30-cheetah-sqnet', runs=5, exe='sqnet-cheetah', end=0, plot=plot)
xc50cs, cc50cs, sc50cs, dc50cs = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-50-cheetah-sqnet', runs=10, exe='sqnet-cheetah', end=0, plot=plot)
print()

xc3ss,  cc3ss,  sc3ss,  dc3ss  = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-3-SCI_HE-sqnet',  runs=1, exe='sqnet-SCI_HE', end=0, plot=plot)
xc14ss, cc14ss, sc14ss, dc14ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-14-SCI_HE-sqnet', runs=5, exe='sqnet-SCI_HE', end=0, plot=plot)
xc30ss, cc30ss, sc30ss, dc30ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-30-SCI_HE-sqnet', runs=5, exe='sqnet-SCI_HE', end=0, plot=plot)
xc50ss, cc50ss, sc50ss, dc50ss = prepare_data(dir='Code/Plots/Results/laptop-desktop/client-50-SCI_HE-sqnet', runs=10, exe='sqnet-SCI_HE', end=0, plot=plot)
print("{}hr {}mins ({}s)".format(round(total_nr/60/60), total_nr%(60*60), round(total_nr, 5)))
total_nr=0

print("server 50-500")# sqnet server 50-500
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
print()

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
print("{}hr {}mins ({}s)".format(round(total_nr/(60*60)), total_nr%(60*60), round(total_nr, 5)))
total_nr=0

print("client 50-500")# sqnet client 50-500
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
print()

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
print("{}hr {}mins ({}s)".format(round(total_nr/(60*60)), total_nr%(60*60), round(total_nr, 5)))
total_nr=0