class Graph:

    def __init__(self):
        self.representation = {}
        self.nb_nodes = 0
        self.nb_edges = 0

    def order(self):
        return self.nb_nodes

    def size(self):
        return self.nb_edges

    def add_node(self, node):
        self.representation[node] = []
        self.nb_nodes += 1

    def add_edge(self, node1, node2, weight=0):
        self.representation[node1].append((node1, node2, weight))
        self.nb_edges += 1

    def node_list(self):
        nodes = []
        for key in self.representation:
            nodes.append(key)
        return nodes

    def get_in_neighbors(self, node):
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
        neighbors = []
        for edge in self.representation[node]:
            neighbors.append(edge[1])
        return neighbors

    def in_degree(self, node):
        return len(self.get_in_neighbors(node))

    def out_degree(self, node):
        return len(self.get_out_neighbors(node))

    def __str__(self):
        return str(self.representation)


if __name__ == '__main__':

    graph = Graph()

    for i in range(5):
        graph.add_node(i)

    for i in range(5):
        for j in range(5):
            if i != j:
                graph.add_edge(i, j)
    print(graph)
    print("In neighbors 0: ", graph.get_in_neighbors(0))
    print("In degree 0: ", graph.in_degree(0))
    print("Out neighbors 0: ", graph.get_out_neighbors(0))
    print("Out neighbors 0: ", graph.out_degree(0))
    print("vertices: ", graph.node_list())

