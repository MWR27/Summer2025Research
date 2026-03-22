from clusters import Clusters, ClusterTracker
import matplotlib.pyplot as plt

cluster_system2 = Clusters({2: 500000})
tracker2 = ClusterTracker(cluster_system2)

tracker2.track_moment(2)
tracker2.run()

xs = tracker2.xs(normalized=True)

k = 2
l = 1

m2_solutions = [(k - l * t) * (k * k - 2 * k * l * t + l * l * t) / (k - 2 * k * t + l * t) for t in xs]

m2s = tracker2.results('m2')
plt.plot(xs, m2s, color='black', linestyle='dashed')
plt.plot(xs, m2_solutions, '-', alpha=.5, color='black')
plt.xlabel('Extent of reaction $t$', fontsize=20)
plt.ylabel('$m_2$', fontsize=20)
plt.show()
print('done!')