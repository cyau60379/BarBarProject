from Graph import Graph


def held_karp(g, start):
    """
    Held-Karp algorithm for the Traveller Salesman Problem
    :param g: a graph
    :param start: the start node
    :return: the distance and the path to go to each node one time and return to start node
    """
    s = g.node_list()
    dist = g.get_dist_matrix()

    if start not in s:
        return None
    else:
        s.remove(start)
        distance, path = rec_held_karp(s, start, dist, [start])
        distance += dist[path[-1]][start]
        path.append(start)
        return distance, path


def rec_held_karp(s, current, dist, path):
    """
    Auxiliary recursive function for the Held-Karp algorithm
    :param list s: list of nodes of the graph that must be reached
    :param current: the current node
    :param dist: the distance matrix of all nodes
    :param path: the path from the start to the current node
    :return: the tuple (distance, path) to go to the next node with the minimum cost
    """
    if len(s) == 1:
        return dist[current][s[0]], path + [s[0]]
    else:
        current_list = []
        for x in s:
            new_s = s[:]
            new_s.remove(x)
            distance, new_path = rec_held_karp(new_s, x, dist, path[:] + [x])
            current_list.append((dist[current][x] + distance, new_path))
        return min(current_list)


if __name__ == '__main__':
    graph = Graph()

    mat = [[0, 100, 1, 100, 2, 100],
           [100, 0, 1, 2, 100, 100],
           [1, 1, 0, 100, 100, 100],
           [100, 2, 100, 0, 100, 1],
           [2, 100, 100, 100, 0, 1],
           [100, 100, 100, 1, 1, 0]]

    for i in range(6):
        graph.add_node(i)

    for i in range(6):
        for j in range(6):
            if i != j:
                graph.add_edge(i, j, mat[i][j])
    print(held_karp(graph, 0))
