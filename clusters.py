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
from scipy.interpolate import make_smoothing_spline
import numpy as np

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

    def kneedle(self, name):
        spl = make_smoothing_spline([i / self._collisions for i in range(self._collisions)], self._trackers[name][1], lam=0)
        x_cont = np.arange(0, 1, 0.01)

import itertools

def find_combos(cluster_counts: dict):
    cluster_list = []
    for cluster_size, cluster_count in cluster_counts.items():
        for i in range(cluster_count):
            cluster_list.append(cluster_size)
    particle_count = 0
    for cluster_size, cluster_count in cluster_counts.items():
        particle_count += cluster_size * cluster_count
    possible_products = set(cluster_counts.keys())
    combos = itertools.combinations_with_replacement(possible_products, 2)
    filtered = set(filter(lambda t: is_valid_combo(t, cluster_counts, particle_count), combos))
    return filtered

def idk(cluster_counts: dict, removals, level=0) -> set:
    if not cluster_counts or (len(cluster_counts) == 1 and next(iter(cluster_counts.values())) == 1):
        return set()
    else:
        particle_count = 0
        for cluster_size, cluster_count in cluster_counts.items():
            particle_count += cluster_size * cluster_count
        possible_products = set()
        combos = filter(lambda t: is_valid_combo(t, cluster_counts, particle_count), itertools.combinations_with_replacement(cluster_counts.keys(), 2))
        for t in combos:
            print(t)
            possible_products.add(t)
            d = cluster_counts.copy()
            if d[t[0]] == 1:
                del d[t[0]]
            else:
                d[t[0]] -= 1
            if d[t[1]] == 1:
                del d[t[1]]
            else:
                d[t[1]] -= 1
            if t[0] + t[1] in d:
                d[t[0] + t[1]] += 1
            else:
                d[t[0] + t[1]] = 1
            
            possible_products.update(idk(d, level + 1))
        print(level)
        return possible_products
    
def potential_reactions(cluster_counts: dict, removals) -> set:
    if not cluster_counts or (len(cluster_counts) == 1 and next(iter(cluster_counts.values())) == 1):
        return set()
    else:
        particle_count = 0
        possible_reactions = set()
        possible_products = set()
        for cluster_size in cluster_counts.keys():
            for i in range(cluster_size, cluster_size * cluster_counts[cluster_size], cluster_size):
                for j in range(i, cluster_size * cluster_counts[cluster_size] - (i - cluster_size), cluster_size):
                    possible_reactions.add((i, j))
                    possible_products.add(i + j)
        return possible_reactions

def possible_reactions(cluster_counts: dict, removals=0) -> set:
    sizes = list(cluster_counts.keys())
    possible_reactions = set()
    for i in range(len(sizes)):
        for j in range(i, len(sizes)):
            if (i != j or cluster_counts[sizes[i]] >= 2) and sizes[i] + sizes[j] - removals >= 0:
                possible_reactions.add((sizes[i], sizes[j], sizes[i] + sizes[j] - removals))
    return possible_reactions

def is_valid_combo(t: tuple, d: dict, particle_count: int) -> bool:
    if t[0] == t[1]:
        return d[t[0]] >= 2 and t[0] + t[1] <= particle_count
    else:
        return t[0] + t[1] <= particle_count

# incomplete
def min_steps_to_produce(target_value, cluster_counts: dict, removals=0) -> int:
    return _change_making(cluster_counts.keys(), target_value)

# copied from Wikipedia
def _get_change_making_matrix(set_of_coins, r: int):
    m = [[0 for _ in range(r + 1)] for _ in range(len(set_of_coins) + 1)]
    for i in range(1, r + 1):
        m[0][i] = math.inf  # By default there is no way of making change
    return m

def _change_making(coins, n: int):
    """This function assumes that all coins are available infinitely.
    if coins are only to be used once, change m[c][r - coin] to m[c - 1][r - coin].
    n is the number to obtain with the fewest coins.
    coins is a list or tuple with the available denominations.
    """
    m = _get_change_making_matrix(coins, n)
    for c, coin in enumerate(coins, 1):
        for r in range(1, n + 1):
            # Just use the coin
            if coin == r:
                m[c][r] = 1
            # coin cannot be included.
            # Use the previous solution for making r,
            # excluding coin
            elif coin > r:
                m[c][r] = m[c - 1][r]
            # coin can be used.
            # Decide which one of the following solutions is the best:
            # 1. Using the previous solution for making r (without using coin).
            # 2. Using the previous solution for making r - coin (without
            #      using coin) plus this 1 extra coin.
            else:
                m[c][r] = min(m[c - 1][r], 1 + m[c][r - coin])
    return m[-1][-1]
