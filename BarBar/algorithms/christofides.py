import GraphStructure.Graph as graph


def christofides(graph, start, iterations, price=0):
    sorted_distances = sort_closest_bars(graph.adjacency_matrix)

    visited = [start]

    length = 0
    path = [start]
    current = start
    # loops until the selected number of bars have been visited
    for bar in range(iterations):
        next_bar = find_next_bar(current, sorted_distances, visited)

        path.append(next_bar)
        visited.append(next_bar)
        length += graph.adjacency_matrix[current][next_bar]
        current = next_bar

    length += graph.adjacency_matrix[path[-1]][start]
    path.append(start)
    print("Result path: ", path)
    print("Result length of the path: ", length)

    return length, path


def sort_closest_bars(adjacency_matrix):
    result = {}

    for key, value in adjacency_matrix.items():
        result[key] = {k: v for k, v in sorted(value.items(), key=lambda item: item[1])}

    return result


def find_next_bar(current, adjacency_matrix, visited):
    for key, value in adjacency_matrix[current].items():
        next_bar = key
        if next_bar not in visited:
            return next_bar
    return 0


if __name__ == '__main__':
    graph = graph.Graph()
    graph.build_graph()

    christofides(graph, 0, 5)
