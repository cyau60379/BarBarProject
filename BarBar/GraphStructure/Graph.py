import jsonParsing.json_parser as parser
from math import sqrt


class Graph:

    def __init__(self):
        self.node_dict = {}
        self.adjacency_matrix = {}
        self.nb_nodes = 0
        self.nb_edges = 0

    def order(self):
        return self.nb_nodes

    def size(self):
        return self.nb_edges

    def add_node(self, node):
        if node not in self.node_dict:
            self.adjacency_matrix[node] = {node: 999999}
            for other_node in self.node_list():
                self.adjacency_matrix[other_node][node] = 999999
                self.adjacency_matrix[node][other_node] = 999999
            self.node_dict[node] = []
            self.nb_nodes += 1
        else:
            pass

    def add_node_bar(self, node, index):

        id = index

        self.adjacency_matrix[id] = {id: 999999}

        for other_node in self.node_list():
            other_bar = self.node_dict[other_node]
            distance = self.distance_between(node, other_bar)

            self.adjacency_matrix[other_node][id] = distance
            self.adjacency_matrix[id][other_node] = distance
            self.nb_edges += 1

        self.node_dict[id] = node
        self.nb_nodes += 1

    def distance_between(self, bar1, bar2):

        lat1 = bar1["latitude"]
        lat2 = bar2["latitude"]

        long1 = bar1["longitude"]
        long2 = bar2["longitude"]

        distance = sqrt((lat2 - lat1) ** 2 + (long2 - long1) ** 2)
        return distance

    def add_edge(self, node1, node2, weight=999999):
        if not self.is_existing_edge(node1, node2):
            self.node_dict[node1].append((node1, node2, weight))
            self.nb_edges += 1
            self.adjacency_matrix[node1][node2] = weight
        else:
            pass

    def node_list(self):
        nodes = []
        for key in self.node_dict:
            nodes.append(key)
        return nodes

    def node_list_price(self, start, price):
        nodes = []
        for key in self.node_dict:
            if key != start:
                reward = 1 - self.adjacency_matrix[key][start]
                if 'price' in self.node_dict[key]:
                    key_price_split = self.node_dict[key]['price'].split(',')
                    try:
                        key_price = key_price_split[0] + "." + key_price_split[1]
                    except:
                        key_price = key_price_split[0]
                    if float(key_price) <= float(price):
                        reward += 1
                nodes.append((key, reward))
        return [(start, 0)] + nodes

    def get_in_neighbors(self, node):
        if node not in self.node_dict:
            raise IndexError
        else:
            neighbors = []
            for key in self.node_dict:
                if key == node:
                    continue
                for edge in self.node_dict[key]:
                    if node in edge:
                        neighbors.append(key)
                        break
            return neighbors

    def get_out_neighbors(self, node):
        if node not in self.node_dict:
            raise IndexError
        else:
            neighbors = []
            for edge in self.node_dict[node]:
                neighbors.append(edge[1])
            return neighbors

    def in_degree(self, node):
        return len(self.get_in_neighbors(node))

    def out_degree(self, node):
        return len(self.get_out_neighbors(node))

    def edge_list(self):
        edges = []
        for key in self.node_dict:
            for edge in self.node_dict[key]:
                edges.append(edge)
        return edges

    def edge_bar_list(self, start):
        edges = []
        for bar in self.adjacency_matrix[start]:
            edges.append(((start, self.node_dict[start]), (bar, self.node_dict[bar]), self.adjacency_matrix[start][bar]))
        return edges

    def build_sub_graph(self, bars):
        for index, bar in enumerate(bars):
            self.add_node_bar(bar, index)

    def get_dist_matrix(self):
        return self.adjacency_matrix

    def is_existing_edge(self, node1, node2):
        exists = False
        for tup in self.node_dict[node1]:
            if tup[1] == node2:
                exists = True
                break
        return exists

    def build_graph(self):
        bars = parser.load_bars("../jsonParsing/bars_complete.json")

        for index, bar in enumerate(bars):
            self.add_node_bar(bar, index)

    def __str__(self):
        return str(self.adjacency_matrix)


"""
if __name__ == '__main__':

    graph = Graph()
    graph.buildGraph()

    print(graph)
    print("In neighbors 0: ", graph.get_in_neighbors(0))
    print("In degree 0: ", graph.in_degree(0))
    print("Out neighbors 0: ", graph.get_out_neighbors(0))
    print("Out neighbors 0: ", graph.out_degree(0))
    print("vertices: ", graph.node_list())
"""
