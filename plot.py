import matplotlib.pyplot as plt
import pickle
from IPython import embed
import numpy as np


statuses = pickle.load(open('statuses.p', 'rb'))

to_plot = [[],[]]
unspent = []
for height in statuses.keys():
    if statuses[height]['spent']:
        to_plot[0].append(height)
        to_plot[1].append(statuses[height]['status']['block_height']-height)
    else:
        unspent.append(height)

plt.scatter(to_plot[0], np.log10(to_plot[1]), alpha=0.2)
yl = plt.ylim()
for unsp in unspent:
    plt.plot([unsp, unsp], yl, color="red", alpha=0.1)
plt.ylim(yl)
plt.figure()
plt.hist(np.log10(to_plot[1]), bins=200)
plt.show()
