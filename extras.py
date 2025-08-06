import itertools
from scipy.interpolate import make_smoothing_spline
import numpy as np

def kneedle(self, name):
    spl = make_smoothing_spline([i / self._collisions for i in range(self._collisions)], self._trackers[name][1], lam=0)
    x_cont = np.arange(0, 1, 0.01)

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
