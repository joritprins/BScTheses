"""
Prints the begin and end time of the results. Also shows run-time.
"""
__author__ = "Jorit Prins"

# Insert path for functions.py file
import sys
sys.path.insert(0, '{}/..'.format(sys.path[0]))
sys.path.insert(0, '{}/../..'.format(sys.path[0]))

import numpy as np
import json
import datetime
from functions import filter_results

total_nr = 0
def read_files(dir: str, name1: str, name2: str):
    time1 = np.array(json.loads(open('{}/{}.json'.format(dir, name1),'r').read().replace('\n', '')))[0 ]['host']['timestamp']
    start = datetime.datetime.fromtimestamp(time1)
    time2 = np.array(json.loads(open('{}/{}.json'.format(dir, name2),'r').read().replace('\n', '')))[-1]['host']['timestamp']
    end   = datetime.datetime.fromtimestamp(time2)
    diff = end-start
    # diff = datetime.sdatetime(end - start)

    return ("{:<2}:{:<2} - {:<2}:{:<2} ({}/{}, {}/{}) -> {}".format(start.hour, start.minute, end.hour, end.minute, start.day, start.month, end.day, end.month, str(diff)))

print("server, 100: ",read_files(dir='Code/Plots/Results/laptop-desktop/server-100-SCI_HE-sqnet', name1='client_1', name2='client_15'), "normal")
print("server, 150: ",read_files(dir='Code/Plots/Results/laptop-desktop/server-150-SCI_HE-sqnet', name1='client_1', name2='client_15'), "normal")
print("server, 200: ",read_files(dir='Code/Plots/Results/laptop-desktop/server-200-SCI_HE-sqnet', name1='client_1', name2='client_15'), "low")
print("server, 400: ",read_files(dir='Code/Plots/Results/laptop-desktop/server-400-SCI_HE-sqnet', name1='client_1', name2='client_15'), "high")
print("client, 100: ",read_files(dir='Code/Plots/Results/laptop-desktop/client-100-SCI_HE-sqnet', name1='client_1', name2='client_10'), "very low")
print("client, 150: ",read_files(dir='Code/Plots/Results/laptop-desktop/client-150-SCI_HE-sqnet', name1='client_1', name2='client_10'), "low")
print("client, 200: ",read_files(dir='Code/Plots/Results/laptop-desktop/client-200-SCI_HE-sqnet', name1='client_1', name2='client_10'), "normal")
print("client, 400: ",read_files(dir='Code/Plots/Results/laptop-desktop/client-400-SCI_HE-sqnet', name1='client_1', name2='client_10'), "normal")

print()
print()

print("cheetah, 3:  ",read_files(dir='Code/Plots/Results/laptop-desktop/client-3-cheetah-sqnet', name1='client_1', name2='client_5'), "normal")
print("cheetah, 14: ",read_files(dir='Code/Plots/Results/laptop-desktop/client-14-cheetah-sqnet', name1='client_1', name2='client_5'), "low")
print("cheetah, 30: ",read_files(dir='Code/Plots/Results/laptop-desktop/client-30-cheetah-sqnet', name1='client_1', name2='client_5'), "normal")
print("sci_he, 3:  ",read_files(dir='Code/Plots/Results/laptop-desktop/client-3-SCI_HE-sqnet', name1='client_1', name2='client_1'), "normal")
print("sci_he, 14: ",read_files(dir='Code/Plots/Results/laptop-desktop/client-14-SCI_HE-sqnet', name1='client_1', name2='client_5'), "low")
print("sci_he, 30: ",read_files(dir='Code/Plots/Results/laptop-desktop/client-30-SCI_HE-sqnet', name1='client_1', name2='client_5'), "normal")


