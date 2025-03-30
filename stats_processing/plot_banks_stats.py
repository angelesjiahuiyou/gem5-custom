import sys
import re
import numpy as np
import matplotlib.pyplot as plt

gem5Log = sys.argv[1]
blockedBanks = list()
labels = list()
explode = list()

try:
    in_file = open(gem5Log, 'r')
    counter = 0

    for line in in_file.readlines():
        parsed = re.sub('\s+',',',line).split(',')
        if parsed[0].find("system.l2.concurrent_banks_ticks") != -1:
            blockedBanks.append(int(parsed[1]))
    sizes =  [x / blockedBanks[-1] * 100 for x in blockedBanks]
    blockedBanks.pop()
    
    for i in range(0, len(blockedBanks)):
        labels.append(str(i) + " banks")
        explode.append(0.03)

    x = np.linspace(0, len(blockedBanks) - 1, len(blockedBanks))
    plt.pie(blockedBanks, explode=explode)
    plt.title('Banks utilization')
    plt.legend(labels=['%s, %1.1f %%' % (l, s) for l, s in zip(labels, sizes)], loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
finally:
    in_file.close()
