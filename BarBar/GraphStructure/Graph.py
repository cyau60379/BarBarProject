import jsonParser as parser
from math import sqrt

class Graph:

    def __init__(self):
        self.representation = {}
        self.dist = {}
        self.nb_nodes = 0
        self.nb_edges = 0

    def order(self):
        return self.nb_nodes

    def size(self):
        return self.nb_edges

    def add_node(self, node):
        if node not in self.representation:
            self.dist[node] = {node: 999}
            for other_node in self.node_list():
                self.dist[other_node][node] = 999
                self.dist[node][other_node] = 999
            self.representation[node] = []
            self.nb_nodes += 1
        else:
            pass


    def add_node_bar(self, node, index):

        id = index

        self.dist[id] = {id: 999}

        for other_node in self.node_list():

            other_bar = self.representation[other_node]
            distance = self.distance_between(node, other_bar)

            self.dist[other_node][id] = distance
            self.dist[id][other_node] = distance

        self.representation[id] = node
        self.nb_nodes += 1

    
    def distance_between(self, bar1, bar2):

        lat1 = bar1["latitude"]
        lat2 = bar2["latitude"]

        long1 = bar1["longitude"]
        long2 = bar2["longitude"]

        distance = dist = sqrt( (lat2 - lat1)**2 + (long2 - long1)**2 )
        return distance


    def add_edge(self, node1, node2, weight=999):
        if not self.is_existing_edge(node1, node2):
            self.representation[node1].append((node1, node2, weight))
            self.nb_edges += 1
            self.dist[node1][node2] = weight
        else:
            pass

    def node_list(self):
        nodes = []
        for key in self.representation:
            nodes.append(key)
        return nodes

    def get_in_neighbors(self, node):
        if node not in self.representation:
            raise IndexError
        else:
            neighbors = []
            for key in self.representation:
                if key == node:
                    continue
                for edge in self.representation[key]:
                    if node in edge:
                        neighbors.append(key)
                        break
            return neighbors

    def get_out_neighbors(self, node):
        if node not in self.representation:
            raise IndexError
        else:
            neighbors = []
            for edge in self.representation[node]:
                neighbors.append(edge[1])
            return neighbors

    def in_degree(self, node):
        return len(self.get_in_neighbors(node))

    def out_degree(self, node):
        return len(self.get_out_neighbors(node))

    def edge_list(self):
        edges = []
        for key in self.representation:
            for edge in self.representation[key]:
                edges.append(edge)
        return edges

    def get_dist_matrix(self):
        return self.dist

    def is_existing_edge(self, node1, node2):
        exists = False
        for tup in self.representation[node1]:
            if tup[1] == node2:
                exists = True
                break
        return exists

    def buildGraph(self):
        bars = parser.loadBars("jsonParsing/barsComplete.json")

        for index, bar in enumerate(bars):
            self.add_node_bar(bar, index)

    def __str__(self):
        return str(self.representation)


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
