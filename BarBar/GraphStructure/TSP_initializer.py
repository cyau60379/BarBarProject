import itertools
from GraphStructure.Graph import Graph

# TODO: load the complete JSON


def tsp_executor(algorithm, address, bar_number, price, bars=None):
    graph, start = initialize_problem(address, bar_number, price)
    distance, path = algo_for_combinations(graph, start, algorithm, bar_number)
    bar_location = []
    result_text = "========== RESULTS ===========\n" \
                  "Algorithm: {}\n" \
                  "Number of bars: {}\n" \
                  "Price: {}\n" \
                  "Time execution: {}\n\n" \
                  "-------- BARS\n".format("Held-Karp", bar_number, price, 1.0)
    for i in range(len(path)):
        result_text += str(i + 1) + "." + bars['bars'][path[i]]['name'] + "(" + bars['bars'][path[i]]['address'] + ")\n"
        bar_location.append((bars['bars'][path[i]]['longitude'], bars['bars'][path[i]]['latitude']))
    result_text += "\n"
    # return bar_location, result_text
    # TODO: Remove the following line
    return [(2.338028, 48.861147), (2.35005, 48.852937)], result_text


def initialize_problem(address, bar_number, price):
    
    return None, None


def find_combinations(s, m):
    """
    Function which find all possible subsets from a set (not all the permutations)
    :param tuple s: set to be tested
    :param int m: subsets length
    :return: a list containing sets of combinations
    """
    return list(itertools.combinations(s, m))


def algo_for_combinations(graph, start, algorithm, bar_number):
    edge_list = graph.edge_bar_list()
    remaining_bars = []
    min_dist = 9999
    min_path = []
    for i in range(edge_list):
        if edge_list[i][2] < 200:
            remaining_bars.append(edge_list[i][1])
    combinations = find_combinations(tuple(remaining_bars), bar_number)
    for combination in combinations:
        comb = [edge_list[0]] + list(combination)
        g = Graph()
        g.build_sub_graph(comb)
        distance, path = algorithm(graph, start)
        if distance < min_dist:
            min_dist = distance
            min_path = path[:]
    return min_dist, min_path
