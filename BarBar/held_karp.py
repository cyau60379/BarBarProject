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
        is_possible = False
        for i in range(len(dist)):
            if dist[i][start] != 999:
                is_possible = True
                break
        if is_possible:
            s.remove(start)
            distance, path = rec_held_karp(s, start, dist, [start])
            if not path:
                return None
            distance += dist[path[-1]][start]
            path.append(start)
            return distance, path
        else:
            return None


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
            distance, new_path = rec_held_karp(new_s, x, dist, path[:] + [x])
            current_list.append((dist[current][x] + distance, new_path))
        if not current_list:
            return 999, []
        return min(current_list)


if __name__ == '__main__':
    graph = Graph()

    mat = [[999, 999, 1, 999, 2, 999],
           [999, 999, 1, 999, 999, 999],
           [1, 1, 999, 999, 999, 999],
           [999, 999, 999, 999, 999, 1],
           [2, 999, 999, 999, 999, 1],
           [999, 999, 999, 1, 1, 999]]

    for k in range(6):
        graph.add_node(k)

    for k in range(6):
        for j in range(6):
            if k != j:
                graph.add_edge(k, j, mat[k][j])
    print(held_karp(graph, 0))
    print(graph.get_dist_matrix())


"""
    mat = [[999, 100, 1, 100, 2, 100],
           [100, 999, 1, 2, 100, 100],
           [1, 1, 999, 100, 100, 100],
           [100, 2, 100, 999, 100, 1],
           [2, 100, 100, 100, 999, 1],
           [100, 100, 100, 1, 1, 999]]"""