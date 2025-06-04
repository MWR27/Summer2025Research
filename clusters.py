import random

class Clusters:
    def __init__(self, cluster_counts):
        self._cluster_counts = cluster_counts.copy()
        self._collision_count = 0
        self._particle_count = 0
        self._weights = {}
        for cluster_size, cluster_count in self._cluster_counts.items():
            total_particle_count = cluster_size * cluster_count
            self._particle_count += total_particle_count
            self._weights[cluster_size] = total_particle_count

    @classmethod
    def create_monomers(cls, count: int):
        return cls({1: count})

    def __str__(self):
        return str(self._cluster_counts)

    def particle_count(self):
        return self._particle_count

    def cluster_counts(self):
        return self._cluster_counts.copy()

    def cluster_count(self, cluster_size: int) -> int:
        if cluster_size in self._cluster_counts:
            return self._cluster_counts[cluster_size]
        else:
            return 0

    def collision_count(self) -> int:
        return self._collision_count

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
        self._particle_count += cluster_size

    def remove_cluster(self, cluster_size: int):
        if cluster_size in self._cluster_counts:
            if self._cluster_counts[cluster_size] == 1:
                del self._cluster_counts[cluster_size]
                del self._weights[cluster_size]
            else:
                self._cluster_counts[cluster_size] -= 1
                self._weights[cluster_size] -= cluster_size
            self._particle_count -= cluster_size
        else:
            raise ValueError(f'no cluster of size {cluster_size} in group of clusters')

import matplotlib.pyplot as plt
import math
from scipy.interpolate import make_smoothing_spline
import numpy as np

class ClusterTracker:
    def __init__(self, clusters, normalize=False):
        self._clusters = clusters
        self._trackers = {}
        self._collisions = 0
        self._normalize = normalize
        self._initial_particle_count = self._clusters.particle_count()

    def add_tracker(self, name, f):
        self._trackers[name] = (lambda: f(self._clusters), [])

    def run(self, limit=math.inf, removals=0):
        while not self._clusters.has_one_cluster() and not self._clusters.is_empty() and self._collisions < limit:
            for tup in self._trackers.values():
                result = tup[0]()
                # if data must be normalized
                if self._normalize:
                    result /= self._clusters.particle_count()
                tup[1].append(result)
            self._clusters.collide(1, removals)
            self._collisions += 1

    def plot_against_collisions(self, name):
        x = None
        if self._normalize:
            x = [i / self._collisions for i in range(self._collisions)] # self._initial_particle_count
        else:
            x = [i for i in range(self._collisions)]
        plt.scatter(x, self._trackers[name][1])
        plt.show()

    def kneedle(self):
        pass
