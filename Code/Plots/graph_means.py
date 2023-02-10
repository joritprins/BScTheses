# Insert path for functions.py file
import sys
sys.path.insert(0, '{}/..'.format(sys.path[0]))

import numpy as np
import matplotlib.pyplot as plt
import json
import os
from functions import filter_results
# Clients_3
c_3   = list(zip(*[[0.605, 0.129, 0.476],[2.044, 0.114, 1.930]]))
c_14  = list(zip(*[[0.457, 0.114, 0.342],[1.415, 0.133, 1.283]]))
c_30  = list(zip(*[[0.450, 0.111, 0.339],[1.416, 0.153, 1.262]]))
c_50  = list(zip(*[[0.405, 0.106, 0.299],[0.993, 0.166, 0.827]]))
c_100 = list(zip(*[[0.403, 0.107, 0.296],[0.945, 0.171, 0.773]]))
c_150 = list(zip(*[[0.405, 0.107, 0.298],[0.953, 0.160, 0.793]]))
c_200 = list(zip(*[[0.407, 0.107, 0.300],[0.967, 0.148, 0.819]])) 
c_400 = list(zip(*[[0.405, 0.108, 0.297],[0.958, 0.157, 0.802]]))
c_500 = list(zip(*[[0.407, 0.107, 0.299],[0.982, 0.175, 0.807]]))

# Server
s_3   = list(zip(*[[0.930, 0.164, 0.766],[2.069, 0.279, 1.790]]))
s_14  = list(zip(*[[0.514, 0.117, 0.398],[1.526, 0.229, 1.297]]))
s_30  = list(zip(*[[0.457, 0.110, 0.347],[1.436, 0.190, 1.246]]))
s_50  = list(zip(*[[0.400, 0.108, 0.292],[1.012, 0.189, 0.823]]))
s_100 = list(zip(*[[0.390, 0.108, 0.281],[0.959, 0.165, 0.793]]))
s_150 = list(zip(*[[0.389, 0.108, 0.280],[0.951, 0.166, 0.786]]))
s_200 = list(zip(*[[0.392, 0.109, 0.283],[0.937, 0.172, 0.765]]))
s_400 = list(zip(*[[0.390, 0.109, 0.281],[0.963, 0.179, 0.784]]))
s_500 = list(zip(*[[0.391, 0.109, 0.282],[0.952, 0.176, 0.776]]))

b_3 = list(zip(*[[0.909, 0.165, 0.744], [4.248, 0.391, 3.857]]))
b_14 = list(zip(*[[0.520, 0.119, 0.401], [1.319, 0.248, 1.071]]))
b_30 = list(zip(*[[0.440, 0.109, 0.331], [1.132, 0.215, 0.917]]))

plt.figure(figsize=(6,4))
# plt.ylim(0, max(np.max(interp_client), np.max(interp_server)))
plt.xlabel("Bandwidth limit (Mbps)")
plt.ylabel("Energy consumption (Wh)")
plt.title("Energy consumption sqnet")
plt.plot([500, 400, 200, 150, 100, 50, 30, 14, 3], [c_500[0][0],c_400[0][0],c_200[0][0],c_150[0][0],c_100[0][0],c_50[0][0],c_30[0][0],c_14[0][0],c_3[0][0]], label="Cheetah (while limiting client)", marker='+')
plt.plot([500, 400, 200, 150, 100, 50, 30, 14, 3], [c_500[0][1],c_400[0][1],c_200[0][1],c_150[0][1],c_100[0][1],c_50[0][1],c_30[0][1],c_14[0][1],c_3[0][1]], label="SCI_HE (while limiting client)" , marker='+')
plt.plot([500, 400, 200, 150, 100, 50, 30, 14, 3], [s_500[0][0],s_400[0][0],s_200[0][0],s_150[0][0],s_100[0][0],s_50[0][0],s_30[0][0],s_14[0][0],s_3[0][0]], label="Cheetah (while limiting server)", marker='+')
plt.plot([500, 400, 200, 150, 100, 50, 30, 14, 3], [s_500[0][1],s_400[0][1],s_200[0][1],s_150[0][1],s_100[0][1],s_50[0][1],s_30[0][1],s_14[0][1],s_3[0][1]], label="SCI_HE (while limiting server)" , marker='+')
plt.plot([30, 14, 3], [b_30[0][1],b_14[0][1],b_3[0][1]], label="Cheetah (while limiting both)", c='green')
plt.plot([30, 14, 3], [b_30[1][1],b_14[1][1],b_3[1][1]], label="SCI_HE (while limiting both)", c='lime')
plt.legend()
plt.tight_layout()
# plt.savefig("Code/Plots/{}.png".format(os.path.basename(__file__).partition(".py")[0]))
plt.show()

exit()

b_3  = [[0.899, 0.162, 0.738],[3.013, 0.259, 2.754]]
b_14 = [[0.520, 0.119, 0.401],[1.314, 0.245, 1.070]]
b_30 = [[0.440, 0.109, 0.331],[1.132, 0.215, 0.917]]


plt.figure(figsize=(10,5))
# plt.ylim(0, max(np.max(interp_client), np.max(interp_server)))
plt.xlabel("Bandwidth limit client (Mbps)")
plt.ylabel("Energy consumption (Wh)")
plt.title("Energy consumption sqnet")
plt.plot([500, 400, 200, 150, 100, 50, 30, 14, 3], [s_500[0][0],s_400[0][0],s_200[0][0],s_150[0][0],s_100[0][0],s_50[0][0],s_30[0][0],s_14[0][0],s_3[0][0]], label="Cheetah", c='red')
plt.plot([500, 400, 200, 150, 100, 50, 30, 14, 3], [s_500[1][0],s_400[1][0],s_200[1][0],s_150[1][0],s_100[1][0],s_50[1][0],s_30[1][0],s_14[1][0],s_3[1][0]], label="Cheetah (client)", c="#A2142F")
plt.plot([500, 400, 200, 150, 100, 50, 30, 14, 3], [s_500[2][0],s_400[2][0],s_200[2][0],s_150[2][0],s_100[2][0],s_50[2][0],s_30[2][0],s_14[2][0],s_3[2][0]], label="Cheetah (server)", c="#A2142F", alpha=.6)
plt.plot([500, 400, 200, 150, 100, 50, 30, 14, 3], [s_500[0][1],s_400[0][1],s_200[0][1],s_150[0][1],s_100[0][1],s_50[0][1],s_30[0][1],s_14[0][1],s_3[0][1]], label="SCI_HE", c='green')
plt.plot([500, 400, 200, 150, 100, 50, 30, 14, 3], [s_500[1][1],s_400[1][1],s_200[1][1],s_150[1][1],s_100[1][1],s_50[1][1],s_30[1][1],s_14[1][1],s_3[1][1]], label="SCI_HE (client)", c="#77AC30")
plt.plot([500, 400, 200, 150, 100, 50, 30, 14, 3], [s_500[2][1],s_400[2][1],s_200[2][1],s_150[2][1],s_100[2][1],s_50[2][1],s_30[2][1],s_14[2][1],s_3[2][1]], label="SCI_HE (server)", c="#77AC30", alpha=.6)
plt.legend()
plt.show()

