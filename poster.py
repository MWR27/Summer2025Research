from clusters import Clusters, ClusterTracker
import matplotlib.pyplot as plt
import numpy as np
import math

# simulation
clusters = Clusters({2: 3000000})
for i in range(3):
    clusters.collide(times=700000, removals=1)
    # plotting
    sizes = clusters.cluster_sizes(10)
    count_fracs = [clusters.cluster_count(size) / clusters.initial_cluster_count() for size in sizes]

    plt.plot(sizes, count_fracs, zorder=1, label=f'{clusters.collision_count()} collisions')
plt.xlabel('cluster size')
plt.ylabel('cluster fraction')

plt.legend()
plt.show()
