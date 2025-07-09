from clusters import Clusters, ClusterTracker
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.optimize import curve_fit

# simulation
clusters = Clusters({2: 3000000})
clusters.collide(times=2000000, removals=1)

# plotting
sizes = clusters.cluster_sizes(50)
print(sizes)
counts = [clusters.cluster_count(size) / clusters.initial_cluster_count() for size in sizes]
plt.xscale('log')
plt.yscale('log')
plt.scatter([i for i in clusters.cluster_sizes(50)], counts, zorder=1)
plt.xlabel('Cluster Size')
plt.ylabel('Cluster Count (Scaled)')
popt, pcov = curve_fit(lambda t, a, b: a * t ** b, sizes, counts)
a = popt[0]
b = popt[1]
print(a, b)
x_cont = np.arange(2, 51, 1)
y_fitted = a * (x_cont ** b)
plt.plot(x_cont, y_fitted, zorder=2, color='red')
plt.legend(['Cluster Count (Scaled)', f'$y={a}x^{b}$'])

plt.show()
print("Done!")
