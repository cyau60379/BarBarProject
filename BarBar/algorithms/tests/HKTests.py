import unittest
from algorithms.held_karp import *


class HeldKarpTests(unittest.TestCase):
    def test__recursive_held_karp(self):
        graph = Graph()

        mat = [[999, 100, 1, 100, 2, 100],
               [100, 999, 1, 2, 100, 100],
               [1, 1, 999, 100, 100, 100],
               [100, 2, 100, 999, 100, 1],
               [2, 100, 100, 100, 999, 1],
               [100, 100, 100, 1, 1, 999]]

        for k in range(6):
            graph.add_node(k)

        for k in range(6):
            for j in range(6):
                if k != j:
                    graph.add_edge(k, j, mat[k][j])
        result = recursive_held_karp(graph, 0)
        self.assertEqual(result, (8, [0, 2, 1, 3, 5, 4, 0]))

    def test_dynamic_held_karp(self):
        graph = Graph()

        mat = [[999, 100, 1, 100, 2, 100],
               [100, 999, 1, 2, 100, 100],
               [1, 1, 999, 100, 100, 100],
               [100, 2, 100, 999, 100, 1],
               [2, 100, 100, 100, 999, 1],
               [100, 100, 100, 1, 1, 999]]

        for k in range(6):
            graph.add_node(k)

        for k in range(6):
            for j in range(6):
                if k != j:
                    graph.add_edge(k, j, mat[k][j])
        result = dynamic_held_karp(graph, 0)
        self.assertEqual(result, (8, [0, 2, 1, 3, 5, 4, 0]))

    def test_parallel_held_karp(self):
        graph = Graph()

        mat = [[999, 100, 1, 100, 2, 100],
               [100, 999, 1, 2, 100, 100],
               [1, 1, 999, 100, 100, 100],
               [100, 2, 100, 999, 100, 1],
               [2, 100, 100, 100, 999, 1],
               [100, 100, 100, 1, 1, 999]]

        for k in range(6):
            graph.add_node(k)

        for k in range(6):
            for j in range(6):
                if k != j:
                    graph.add_edge(k, j, mat[k][j])
        result = parallel_held_karp(graph, 0)
        self.assertEqual(result, (8, [0, 2, 1, 3, 5, 4, 0]))

    def test_recursive_held_karp_without_solution(self):
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
        result = recursive_held_karp(graph, 0)
        self.assertEqual(result, None)

    def test_recursive_held_karp_empty_graph(self):
        graph = Graph()
        result = recursive_held_karp(graph, 0)
        self.assertEqual(result, None)

    def test_recursive_held_karp_isolated_start(self):
        graph = Graph()

        mat = [[999, 999, 1, 999, 2, 999],
               [999, 999, 1, 999, 999, 999],
               [999, 1, 999, 999, 999, 999],
               [999, 999, 999, 999, 999, 1],
               [999, 999, 999, 999, 999, 1],
               [999, 999, 999, 1, 1, 999]]

        for k in range(6):
            graph.add_node(k)

        for k in range(6):
            for j in range(6):
                if k != j:
                    graph.add_edge(k, j, mat[k][j])
        result = recursive_held_karp(graph, 0)
        self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
