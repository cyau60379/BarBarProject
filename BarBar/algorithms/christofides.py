import GraphStructure.Graph as graph


def christofides(graph, start, iterations):
    sorted_distances = sort_closest_bars(graph.dist)

    visited = [start]

    length = 0
    path = [start]

    # loops until the selected number of bars have been visited
    for bar in range(iterations - 1):
        next_bar = find_next_bar(start, sorted_distances, visited)

        path.append(next_bar)
        visited.append(next_bar)
        length += graph.dist[start][next_bar]
        start = next_bar

    print("Result path: ", path)
    print("Result length of the path: ", length)

    return length, path


def sort_closest_bars(dist):
    result = {}

    for key, value in dist.items():
        result[key] = {k: v for k, v in sorted(value.items(), key=lambda item: item[1])}

    return result


def find_next_bar(current, dist, visited):
    for key, value in dist[current].items():
        next_bar = key
        if next_bar not in visited:
            return next_bar
    return 0


if __name__ == '__main__':
    graph = graph.Graph()
    graph.build_graph()

    christofides(graph, 0, 5)
