import itertools
from geopy.geocoders import Nominatim
import jsonParsing.json_parser as parser

from GraphStructure.Graph import Graph

BARS = parser.load_bars("../jsonParsing/bars_complete.json")


def tsp_executor(algorithm, address, bar_number, price):
    graph, start = initialize_problem(address)
    distance, path, min_graph = algo_for_combinations(graph, start, algorithm, bar_number)
    bar_location = []
    result_text = "========== RESULTS ===========\n" \
                  "Algorithm: {}\n" \
                  "Number of bars: {}\n" \
                  "Price: {}\n" \
                  "Time execution: {}\n\n" \
                  "-------- BARS\n".format("Held-Karp", bar_number, price, "1.0")
    print(min_graph.representation)
    for i in path:
        result_text += str(i + 1) + "." + min_graph.representation[i]['name'] + "(" + min_graph.representation[i][
            'address'] + ")\n"
        bar_location.append((min_graph.representation[i]['longitude'], min_graph.representation[i]['latitude']))
    result_text += "\n"
    return bar_location, result_text
    # TODO: Remove the following line
    # return [(2.338028, 48.861147), (2.35005, 48.852937)], result_text


def initialize_problem(address):
    graph = Graph()
    graph.build_graph()
    print("Bar Graph ok")
    position = {'name': 'Your position',
                'address': address}
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(address)

    if location:
        position["latitude"] = location.latitude
        position["longitude"] = location.longitude
    else:
        print("could not locate bar %s" % address)
    graph.add_node_bar(position, 800)
    print("Bar Graph + position ok")
    return graph, 800


def find_combinations(s, m):
    """
    Function which find all possible subsets from a set (not all the permutations)
    :param tuple s: set to be tested
    :param int m: subsets length
    :return: a list containing sets of combinations
    """
    return list(itertools.combinations(s, m))


def algo_for_combinations(graph, start, algorithm, bar_number):
    edge_list = graph.edge_bar_list(start)
    print("Edge list ok")
    remaining_bars = []
    min_dist = 9999
    min_path = []
    min_graph = Graph()
    for i in range(len(edge_list)):
        if edge_list[i][2] * 1000 < 3:
            remaining_bars.append(edge_list[i][1][1])
    combinations = find_combinations(tuple(remaining_bars), int(bar_number))
    print("Number of candidates: ", len(remaining_bars))
    i = 0
    for combination in combinations:
        comb = [edge_list[0][0][1]] + list(combination)
        g = Graph()
        g.build_sub_graph(comb)
        print("Subgraph ok")
        distance, path = algorithm(g, 0)
        print("Iteration ", i, ": Ok")
        i += 1
        if distance < min_dist:
            min_dist = distance
            min_path = path[:]
            min_graph = g
    return min_dist, min_path, min_graph
