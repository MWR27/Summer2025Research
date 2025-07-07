from clusters import Clusters, ClusterTracker
import matplotlib.pyplot as plt
import numpy as np


# simulation
clusters = Clusters({2: 3000000})
clusters.collide(times=2000000, removals=1)

# plotting
sizes = clusters.cluster_sizes(50)
counts = [clusters.cluster_count(size) / clusters.initial_cluster_count() for size in sizes]
plt.plot(sizes, counts, zorder=2)
plt.xlabel('Cluster Size')
plt.ylabel('Cluster Count (Scaled)')

x_cont = np.arange(2, 50, 1)
decay_func = x_cont ** (-5/2)
plt.plot(x_cont, decay_func, zorder=1)
plt.legend(['Cluster Count (Scaled)', 'Decay Rate'])

plt.show()
print("Done!")
