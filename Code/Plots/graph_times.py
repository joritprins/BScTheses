"""
Graphs the average run-times. Data from times.py
"""
__author__ = "Jorit Prins"

# Insert path for functions.py file
import sys
sys.path.insert(0, '{}/..'.format(sys.path[0]))

import matplotlib.pyplot as plt

# 3- 50 mean
cheetah_server = [1126.8446233987809,285.2745457649231,188.33107235431672,159.09236173629762]
scihe_server =   [10088.009768062167,3415.873621606827,2716.5576629400252,830.4872403621673]
cheetah_client = [572.9158320426941,228.3454137325287,212.19996824264527,141.04780347347258]
scihe_client =   [10710.645370960236,3074.739104223251,2811.7377185821533,806.3151465892792]
plt.figure(figsize=(8,5))
# plt.ylim(0, max(np.max(interp_client), np.max(interp_server)))
plt.xlabel("Bandwidth limit (Mbps)")
plt.ylabel("Run-time (s))")
plt.title("Average run-times of both SNNI's with sqnet")
plt.xlim(0,55)
# plt.ylim(0,900)
plt.plot([3, 14, 30, 50], cheetah_client, label="Cheetah while limiting outgoing bandwidth of client", marker='+')
plt.plot([3, 14, 30, 50], scihe_client, label="SCI_HE while limiting outgoing bandwidth of client", marker='+')
plt.plot([3, 14, 30, 50], cheetah_server, label="Cheetah while limiting outgoing bandwidth of server", marker='+')
plt.plot([3, 14, 30, 50], scihe_server, label="SCI_HE while limiting outgoing bandwidth of server", marker='+')
plt.legend()
plt.tight_layout()
plt.savefig("Code/Plots/graph_times_lower_mean.png")
plt.show()

# 50 - 500 mean
cheetah_client = [141.04780347347258,141.55914857387543,141.3012013196945,142.57435355186462,143.2986139535904,140.66336045265197]
scihe_client =   [806.3151465892792,531.9427059173584,572.8501765012741,618.7988482475281,603.3441677331924,599.2063407182693]
cheetah_server = [159.09236173629762,142.89507441520692,142.11561414400737,145.403901274999,143.22689838409423,146.38538988431296]
scihe_server =   [830.4872403621673,609.6551687558492,591.4580594062805,546.7006603558858,632.5325099627177,624.4942903200786]
plt.figure(figsize=(8,5))
# plt.ylim(0, max(np.max(interp_client), np.max(interp_server)))
plt.xlabel("Bandwidth limit (Mbps)")
plt.ylabel("Run-time (s))")
plt.title("Average run-times of both SNNI's with sqnet")
plt.xlim(0,550)
plt.ylim(0,900)
plt.plot([50, 100, 150, 200, 400, 500], cheetah_client, label="Cheetah while limiting outgoing bandwidth of client", marker='+')
plt.plot([50, 100, 150, 200, 400, 500], scihe_client, label="SCI_HE while limiting outgoing bandwidth of client", marker='+')
plt.plot([50, 100, 150, 200, 400, 500], cheetah_server, label="Cheetah while limiting outgoing bandwidth of server", marker='+')
plt.plot([50, 100, 150, 200, 400, 500], scihe_server, label="SCI_HE while limiting outgoing bandwidth of server", marker='+')
plt.legend()
plt.tight_layout()
plt.savefig("Code/Plots/graph_times_mean.png")
plt.show()

# 50 - 500 median
cheetah_client = [140.7185037136078,141.42507767677307,140.92904937267303,143.75105130672455,142.59341323375702,140.13682508468628] # median
scihe_client = [794.3755844831467,529.1085877418518,580.4118584394455,610.309916973114,597.5288528203964,598.155815243721] # median
cheetah_server = [158.1440405845642,141.9459788799286,140.40858602523804,145.63071060180664,143.8677966594696,143.94542288780212] # median
scihe_server = [831.623149394989,595.8258652687073,592.8012268543243,526.2659387588501,625.4336166381836,590.32422041893] # median
plt.figure(figsize=(8,5))
# plt.ylim(0, max(np.max(interp_client), np.max(interp_server)))
plt.xlabel("Bandwidth limit (Mbps)")
plt.ylabel("Run-time (s))")
plt.title("Median run-times of both SNNI's with sqnet")
plt.xlim(0,550)
plt.ylim(0,900)
plt.plot([50, 100, 150, 200, 400, 500], cheetah_client, label="Cheetah while limiting outgoing bandwidth of client", marker='+')
plt.plot([50, 100, 150, 200, 400, 500], scihe_client, label="SCI_HE while limiting outgoing bandwidth of client", marker='+')
plt.plot([50, 100, 150, 200, 400, 500], cheetah_server, label="Cheetah while limiting outgoing bandwidth of server", marker='+')
plt.plot([50, 100, 150, 200, 400, 500], scihe_server, label="SCI_HE while limiting outgoing bandwidth of server", marker='+')
plt.legend()
plt.tight_layout()
plt.savefig("Code/Plots/graph_times_median.png")
plt.show()