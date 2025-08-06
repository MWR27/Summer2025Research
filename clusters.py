import random
import math

class Clusters:
    def __init__(self, cluster_counts):
        self._cluster_counts = cluster_counts.copy()
        self._collision_count = 0
        self._cluster_count = 0
        self._particle_count = 0
        self._weights = {}
        for cluster_size, cluster_count in self._cluster_counts.items():
            self._cluster_count += cluster_count
            total_particle_count = cluster_size * cluster_count
            self._particle_count += total_particle_count
            self._weights[cluster_size] = total_particle_count
        self._initial_cluster_count = self._cluster_count

    @classmethod
    def create_monomers(cls, count: int):
        return cls({1: count})

    def __str__(self):
        return str(self._cluster_counts)

    def particle_count(self):
        return self._particle_count

    def cluster_counts(self):
        return self._cluster_counts.copy()

    def cluster_count(self, cluster_size: int =None) -> int:
        if cluster_size == None:
            return self._cluster_count
        elif cluster_size in self._cluster_counts:
            return self._cluster_counts[cluster_size]
        else:
            return 0
        
    def initial_cluster_count(self) -> int:
        return self._initial_cluster_count

    def collision_count(self) -> int:
        return self._collision_count

    def cluster_sizes(self, limit: int =math.inf) -> list:
        return [size for size in self._cluster_counts.keys() if size <= limit]

    def cluster_list(self) -> list:
        l = []
        for cluster_size, cluster_count in self._cluster_counts.items():
            l.append([cluster_size] * cluster_count)
        return l

    def has_one_cluster(self):
        return len(self._cluster_counts) == 1 and next(iter(self._cluster_counts.values())) == 1

    def is_empty(self):
        return self.particle_count() == 0

    def collide(self, times: int, removals: int =0) -> int:
        successful_collisions = 0
        for i in range(times):
            if self.has_one_cluster() or self.is_empty():
                break
            else:
                # pick one cluster
                cluster_size_a = random.choices(population=list(self._cluster_counts.keys()), weights=list(self._weights.values()))[0]
                self.remove_cluster(cluster_size_a)
                # pick another cluster
                cluster_size_b = random.choices(population=list(self._cluster_counts.keys()), weights=list(self._weights.values()))[0]
                self.remove_cluster(cluster_size_b)
                if cluster_size_a + cluster_size_b - removals > 0:
                    self.add_cluster(cluster_size_a + cluster_size_b - removals)
                elif cluster_size_a + cluster_size_b - removals < 0:
                    self.add_cluster(cluster_size_a)
                    self.add_cluster(cluster_size_b)
                    raise RuntimeError(f'combined cluster size ({cluster_size_a} and {cluster_size_b}) smaller than required loss per collision ({removals})')
                successful_collisions += 1
        self._collision_count += successful_collisions
        return successful_collisions

    def add_cluster(self, cluster_size: int):
        if cluster_size in self._cluster_counts:
            self._cluster_counts[cluster_size] += 1
            self._weights[cluster_size] += cluster_size
        elif cluster_size > 0:
            self._cluster_counts[cluster_size] = 1
            self._weights[cluster_size] = cluster_size
        else:
            raise ValueError(f'cannot have cluster of size {cluster_size} in group of clusters')
        self._cluster_count += 1
        self._particle_count += cluster_size

    def remove_cluster(self, cluster_size: int):
        if cluster_size in self._cluster_counts:
            if self._cluster_counts[cluster_size] == 1:
                del self._cluster_counts[cluster_size]
                del self._weights[cluster_size]
            else:
                self._cluster_counts[cluster_size] -= 1
                self._weights[cluster_size] -= cluster_size
            self._cluster_count -= 1
            self._particle_count -= cluster_size
        else:
            raise ValueError(f'no cluster of size {cluster_size} in group of clusters')

import matplotlib.pyplot as plt

class ClusterTracker:
    def __init__(self, clusters):
        self._clusters = clusters
        self._trackers = {}
        self._collisions = 0
        self._initial_cluster_count = self._clusters.cluster_count()
        self._initial_particle_count = self._clusters.particle_count()

    def add_tracker(self, name, f, normalize=None):
        norm_func = None
        if normalize != None:
            norm_func = lambda i: normalize(self._clusters, i)
        self._trackers[name] = (lambda: f(self._clusters), [], norm_func)

    def run(self, limit=math.inf, removals=0):
        while not self._clusters.has_one_cluster() and not self._clusters.is_empty() and self._collisions < limit:
            for tup in self._trackers.values():
                result = tup[0]()
                # if data must be normalized
                if tup[2] != None:
                    result = tup[2](result)
                tup[1].append(result)
            self._clusters.collide(1, removals)
            self._collisions += 1

    def plot_against_collisions(self, name):
        x = None
        if self._trackers[name][2] == None:
            x = [i for i in range(self._collisions)]
        else:
            x = [i / self._initial_cluster_count for i in range(self._collisions)] # self._initial_particle_count
        plt.scatter(x, self._trackers[name][1])
        plt.xlabel('collision fraction')
        plt.ylabel(name)
        plt.show()
