from clusters import Clusters
import matplotlib.pyplot as plt
'''
def plot_against_collisions(clusters, f, count, removals=0):
    x = [i for i in range(count + 1)]
    y = []
    for i in range(count + 1):
        y.append(f(i))
        clusters.collide(1, removals)
    plt.scatter(x, y)
    plt.show()
'''

def plot_against_collisions2(clusters, f, removals=0):
    x = []
    y = []
    i = 0
    while not clusters.has_one_cluster() and not clusters.is_empty():
        x.append(i)
        y.append(f(i))
        i += 1
        clusters.collide(1, removals)
    plt.scatter(x, y)
    plt.show()

clusters = Clusters({2: 100000})
clusters.collide(100000, 1)

data1 = clusters.cluster_list()
plt.hist(data1)
plt.show()

clusters2 = Clusters({2: 100000})

plot_against_collisions2(clusters2, lambda i: clusters2.cluster_count(2), 1)

def max_cluster_size(clusters):
    c_keys = clusters.cluster_counts().keys()
    if len(c_keys) > 0:
        return max(c_keys)
    else:
        return 0

clusters3 = Clusters({2: 100000})

plot_against_collisions2(clusters3, lambda i: max_cluster_size(clusters3), 1)
