"""
Prints the overhead caused by scaphandre of one run
"""
__author__ = "Jorit Prins"

# Insert path for functions.py file
import sys
sys.path.insert(0, '{}/..'.format(sys.path[0]))

import numpy as np
import matplotlib.pyplot as plt
import json
import os


x_ = np.arange(0, 100, 0.1)
x_y_interp = []
for i in range(1,50):
    json_string = open('Code/Plots/Results/same-device/cheetah-sqnet-50/cheetah-sqnet-{}.json'.format(i), 'r').read().replace('\n', '')

    # Load power measurements and convert to array
    arr = np.array(json.loads(json_string))

    # Find first and last timestamp
    start = arr[0]['host']['timestamp']
    end  = arr[-1]['host']['timestamp']-start

    # Calculate percentage of power usage
    filtered = []
    for measurement in arr:
        tmp = 0 
        sc = 0
        for consumer in measurement['consumers']:  
            if consumer['exe'] == 'scaphandre':
                sc = consumer['consumption']
                tmp += consumer['consumption']
            else:
                tmp += consumer['consumption']
        frac = sc*100/tmp
        perc = (measurement['host']['timestamp']-start)*100/end
        filtered.append((perc, frac))
    
    x_y = np.array(list(zip(*filtered)))
    
    x_y_interp.append(np.interp(x_, x_y[0], x_y[1], left=0, right=0))
    
plt.figure(figsize=(10, 5))
plt.title('Average power consumption of Scaphandre in terms of total power consumption')
plt.xlabel("Percentage of total runtime SNNI (%)")
plt.ylabel("Percentage of total power consumption\n(% of all consumers)")
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.plot(x_, np.mean(x_y_interp, 0), color='b', label='Average power consumption')
plt.plot(x_, np.mean(x_y_interp, 0), color='b', label='Measurements of all runs', alpha=0.3)
plt.plot([x_]*49, x_y_interp, alpha=0.3, color='b')
plt.legend()
plt.savefig("Code/Plots/{}.png".format(os.path.basename(__file__).partition(".py")[0]))
plt.show()