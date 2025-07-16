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
count_fracs = [clusters.cluster_count(size) / clusters.initial_cluster_count() for size in sizes]
log_sizes = [math.log(i) for i in sizes]
log_count_fracs = [math.log(i) for i in count_fracs]

plt.scatter(log_sizes, log_count_fracs, zorder=1)
plt.xlabel('log cluster size')
plt.ylabel('log cluster fraction')

intercept, slope = np.polynomial.polynomial.Polynomial.fit(log_sizes, log_count_fracs, 1).convert().coef
x_cont = np.linspace(math.log(2), math.log(50), 2)
y_fitted = intercept + slope * x_cont
equation = f'$y={intercept}+{slope}x$' if slope >= 0 else f'$y={intercept}-{-slope}x$'
plt.plot(x_cont, y_fitted, zorder=2, color='red', label=equation)
plt.legend()

plt.show()
print("Done!")
