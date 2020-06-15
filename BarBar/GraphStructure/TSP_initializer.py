from GraphStructure.Graph import Graph


def tsp_executor(algorithm, address, bar_number, price):
    graph, start = initialize_graph(address, bar_number, price)
    distance, path = algorithm(graph, start)
    pass


def initialize_graph(address, bar_number, price):
    return None, None
