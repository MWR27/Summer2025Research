from clusters import Clusters, ClusterTracker
import matplotlib.pyplot as plt

cluster_system2 = Clusters({2: 1000000})
tracker2 = ClusterTracker(cluster_system2)

tracker2.track_moment(2)
tracker2.track_moment(3)
tracker2.run(limit=500000, removals=1)

xs = tracker2.xs(normalized=True)

k = 2
l = 1

m2_solutions = [(k - l * t) * (k * k - 2 * k * l * t + l * l * t) / (k - 2 * k * t + l * t) for t in xs]
m3_solutions = [(k*(k - l*t)**3) / (l*(k - 2*k*t + l*t)**3) \
                * ((2*(l - k)**3*k*k)/((k - l*t)*(k - l*t)) + (6*(k-l)**2*(2*k - l)*k)/(k - l*t) + k*k \
                   + (l - k)*(l - k)*(14*k - 8*l)) for t in xs]

plt.xlabel('Extent of reaction $t$', fontsize=20)

m2s = tracker2.results('m2')
m3s = tracker2.results('m3')
plt.plot(xs, m2s, color='black', linestyle='dashed')
plt.plot(xs, m2_solutions, '-', alpha=.5, color='black')
plt.ylabel('$m_2$', fontsize=20)
plt.savefig('dimers_m2.png', dpi=600,bbox_inches='tight')
plt.show()

plt.plot(xs, m3s, color='black', linestyle='dashed')
plt.plot(xs, m3_solutions, '-', alpha=.5, color='black')
plt.ylabel('$m_3$', fontsize=20)
plt.savefig('dimers_m3.png', dpi=600,bbox_inches='tight')
plt.show()

print('done!')
