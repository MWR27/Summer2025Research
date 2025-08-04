from clusters import Clusters, ClusterTracker
import matplotlib.pyplot as plt
import numpy as np
import math

# simulation
clusters = Clusters({1: 1000000, 2: 1000000, 3: 1000000})
for i in range(3):
    clusters.collide(times=666666, removals=2)
    # plotting
    sizes = clusters.cluster_sizes(50)
    count_fracs = [clusters.cluster_count(size) / clusters.initial_cluster_count() for size in sizes]

    plt.scatter(sizes, count_fracs, zorder=1, label=f'{clusters.collision_count()} collisions')
plt.xlabel('cluster size')
plt.ylabel('cluster fraction')

plt.legend()
plt.show()
