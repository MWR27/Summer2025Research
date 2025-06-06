from clusters import Clusters, ClusterTracker
import matplotlib.pyplot as plt
from scipy.interpolate import make_smoothing_spline

import numpy as np
'''
clusters = Clusters({2: 100000})
clusters.collide(100000, 1)

data1 = clusters.cluster_list()
plt.hist(data1)
plt.show()
'''

def max_cluster_size(clusters):
    c_keys = clusters.cluster_counts().keys()
    if len(c_keys) > 0:
        return max(c_keys)
    else:
        return 0

clusters = Clusters({3: 10000, 1: 50000})
tracker = ClusterTracker(clusters)
tracker.add_tracker('cluster count', lambda c: c.cluster_count(1), lambda c, i: i / tracker._initial_cluster_count)
tracker.add_tracker('max cluster size', lambda c: max_cluster_size(c), lambda c, i: i / c.particle_count())

tracker.run(100, removals=2)
plt.hist(clusters.cluster_list())
plt.show()

tracker.run(removals=2)
tracker.plot_against_collisions('cluster count')
tracker.plot_against_collisions('max cluster size')

'''
spl =  make_smoothing_spline([i / tracker2._collisions for i in range(tracker2._collisions)], tracker2._trackers['max cluster size'][1], lam=0)
x_cont = np.arange(0, 1, 0.01)
plt.plot(x_cont, spl(x_cont))
plt.plot(x_cont, x_cont, '-.')
diff_curve = x_cont - spl(x_cont)
plt.plot(x_cont, diff_curve)
plt.show()
'''
