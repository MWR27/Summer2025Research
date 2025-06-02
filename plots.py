from clusters import Clusters
import matplotlib.pyplot as plt
import numpy as np

def plot_against_collisions(clusters, f, count):
    x = [i for i in range(count + 1)]
    y = []
    for i in range(count + 1):
        y.append(f(i))
        clusters.collide(1)
    plt.scatter(x, y)
    plt.show()

clusters = Clusters({1: 10000, 2: 10000})
clusters.collide(10000, 2)

data1 = clusters.cluster_list()
plt.hist(data1)
plt.show()

clusters2 = Clusters({1: 10000, 2: 10000})

plot_against_collisions(clusters2, lambda i: clusters2.cluster_count(1), clusters2.particle_count())

clusters3 = Clusters({1: 10000, 2: 10000})

plot_against_collisions(clusters3, lambda i: max(clusters3.cluster_counts().keys()), clusters3.particle_count())
