import itertools
from multiprocessing import Pool, Manager
from GraphStructure.Graph import Graph


def held_karp(g, start):
    """
    Recursive Held-Karp algorithm for the Traveller Salesman Problem
    :param Graph g: a graph
    :param start: the start node
    :return: the distance and the path to go to each node one time and return to start node
    """
    s = g.node_list()
    dist = g.get_dist_matrix()

    if start not in s:
        return None
    else:
        is_possible = False
        for i in range(len(dist)):
            if dist[i][start] != 999:
                is_possible = True
                break
        if is_possible:
            s.remove(start)
            distance, path = rec_held_karp(s, start, dist, [start], start)
            if not path:
                return None
            return distance, path
        else:
            return None


def rec_held_karp(s, current, dist, path, start):
    """
    Auxiliary recursive function for the Held-Karp algorithm
    :param list s: list of nodes of the graph that must be reached
    :param current: the current node
    :param dist: the distance matrix of all nodes
    :param path: the path from the start to the current node
    :param start:
    :return: the tuple (distance, path) to go to the next node with the minimum cost
    """
    if len(s) == 1:
        if dist[current][s[0]] == 999:
            return 999, []
        return dist[current][s[0]], path + [s[0]]
    else:
        current_list = []
        for x in s:
            if dist[current][x] == 999:
                continue
            new_s = s[:]
            new_s.remove(x)
            distance, new_path = rec_held_karp(new_s, x, dist, path[:] + [x], start)
            current_list.append((dist[current][x] + distance, new_path))
        if not current_list:
            return 999, []
        if current == start:
            try:
                return min(map(lambda tup: add_start_dist(current, dist, tup), current_list))
            except IndexError:
                return 999, []
        else:
            return min(current_list)


def add_start_dist(start, dist, tup):
    """
    Add the start node at the end of the path and calculate the distance of the full path
    :param start: the start node of the circuit
    :param dist: the distance matrix
    :param tup: the current tuple containing the distance and the path
    :return: the new distance with the full path
    """
    new_dist = tup[0] + dist[tup[1][-1]][start]
    final_path = tup[1]
    final_path.append(start)
    return new_dist, final_path


def find_subsets(s, m):
    """
    Function which find all possible subsets from a set (not all the permutations)
    :param tuple s: set to be tested
    :param int m: subsets length
    :return: a list containing sets of combinations
    """
    return list(itertools.combinations(s, m))


def dynamic_held_karp(g, start):
    """
    Dynamic Held-Karp algorithm for the Traveller Salesman Problem
    :param Graph g: a graph
    :param start: the start node
    :return: the distance and the path to go to each node one time and return to start node
    """
    dist_matrix = g.get_dist_matrix()
    nodes = g.node_list()
    nodes.remove(start)
    node_set = tuple(nodes)
    path_dict = {}
    for node in nodes:
        path_dict[((node,), node)] = (dist_matrix[node][start], [node, start])

    for s in range(2, len(nodes) + 1):
        subsets = find_subsets(node_set, s)
        for subset in subsets:
            path_dict_filler(dist_matrix, path_dict, subset)

    distance, path = min([(path_dict[(node_set, m)][0] + dist_matrix[start][m],
                           [start] + path_dict[(node_set, m)][1]) for m in node_set])

    return distance, path


def parallel_held_karp(g, start, processors=3):
    """
    Parallel Held-Karp algorithm for the Traveller Salesman Problem
    :param processors:
    :param Graph g: a graph
    :param start: the start node
    :return: the distance and the path to go to each node one time and return to start node
    """
    dist_matrix = g.get_dist_matrix()
    nodes = g.node_list()
    nodes.remove(start)
    node_set = tuple(nodes)
    manager = Manager()
    path_dict = manager.dict()

    for node in nodes:
        path_dict[((node,), node)] = (dist_matrix[node][start], [node, start])

    for s in range(2, len(nodes) + 1):
        subsets = find_subsets(node_set, s)
        pool = Pool(processors)
        [pool.apply(path_dict_filler, args=(dist_matrix, path_dict, subset)) for subset in subsets]

    distance, path = min([(path_dict[(node_set, m)][0] + dist_matrix[start][m],
                           [start] + path_dict[(node_set, m)][1]) for m in node_set])

    return distance, path


def path_dict_filler(dist_matrix, path_dict, subset):
    for node in subset:
        new_sub = set(subset)
        new_sub.remove(node)
        new_subset = tuple(new_sub)
        path_dict[(subset, node)] = min(
            [(path_dict[(new_subset, m)][0] + dist_matrix[node][m],
              [node] + path_dict[(new_subset, m)][1]) for m in new_subset])
