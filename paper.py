from clusters import Clusters, ClusterTracker
import matplotlib.pyplot as plt
from math import log

cluster_system = Clusters({2: 1000000})
tracker = ClusterTracker(cluster_system)

tracker.track_sizes(2, 3, 4, 5, name='cluster fraction', normalize=lambda clusters, val: val / clusters.initial_cluster_count())
tracker.track_particle_count(name='m1', normalize=lambda clusters, val: val / clusters.initial_cluster_count())
tracker.run(removals=1)

xs = tracker.xs(normalized=True)

m1s = tracker.results('m1')

solutions = {}
solutions[2] = [0.0625 * m1 ** 4 for m1 in m1s]
solutions[3] = [0.03125 * m1 ** 5 - 0.015625 * m1 ** 6 for m1 in m1s]
solutions[4] = [(0.0234375 * (log(2) - 1)) * m1 ** 7 + 0.01171875 * m1 ** 8 - 0.0234375 * log(m1) * m1 ** 7 for m1 in m1s]
solutions[5] = [0.011719 * log(m1) * log(m1) * m1 ** 9 + 0.015981 * log(m1) * m1 ** 9 - 0.013916 * m1 ** 10 + 0.006730 * m1 ** 9 + 0.008789 * m1 ** 8 for m1 in m1s]

for cluster_size in [2, 3]:
    y = tracker.results(f'{cluster_size}-cluster fraction')
    plt.plot(xs, y, label=f'{cluster_size}', color='black', linestyle='dashed')
    if cluster_size in solutions:
        plt.plot(xs, solutions[cluster_size], '-', alpha=.5, color='black')

plt.text(0.15, 0.80, '$u_2$', fontsize=18)
plt.text(0.15, 0.15, '$u_3$', fontsize=18)
#plt.text(0.50, 0.04, '$u_4$', fontsize=18)
#plt.text(0.50, 0.025, '$u_5$', fontsize=18)

plt.xlabel('Extent of reaction $t$', fontsize=20) 
plt.ylabel('Cluster fraction', fontsize=20)

#plt.savefig('dimers_2_3.png', dpi=600,bbox_inches='tight')
plt.show()
