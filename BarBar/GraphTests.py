import io
import sys
import unittest
from Graph import Graph


class GraphTests(unittest.TestCase):
    def test_init(self):
        g = Graph()
        test_list = [(g.representation, {}), (g.dist, {}), (g.nb_nodes, 0), (g.nb_edges, 0)]
        for g_element, expected_value in test_list:
            with self.subTest():
                self.assertEqual(g_element, expected_value)

    def test_order(self):
        g = Graph()
        self.assertEqual(g.order(), 0)

    def test_size(self):
        g = Graph()
        self.assertEqual(g.size(), 0)

    def test_add_node(self):
        g = Graph()
        g.add_node("test")
        test_list = [(g.representation, {"test": []}),
                     (g.dist, {"test": {"test": 999}}),
                     (g.nb_nodes, 1),
                     (g.nb_edges, 0)]
        for g_element, expected_value in test_list:
            with self.subTest():
                self.assertEqual(g_element, expected_value)

    def test_add_the_same_node_twice(self):
        g = Graph()
        g.add_node("test")
        g.add_node("test")
        test_list = [(g.representation, {"test": []}),
                     (g.dist, {"test": {"test": 999}}),
                     (g.nb_nodes, 1),
                     (g.nb_edges, 0)]
        for g_element, expected_value in test_list:
            with self.subTest():
                self.assertEqual(g_element, expected_value)

    def test_add_two_node(self):
        g = Graph()
        g.add_node("test")
        g.add_node("another")
        test_list = [(g.representation, {"test": [], "another": []}),
                     (g.dist, {"test": {"test": 999, "another": 999}, "another": {"test": 999, "another": 999}}),
                     (g.nb_nodes, 2),
                     (g.nb_edges, 0)]
        for g_element, expected_value in test_list:
            with self.subTest():
                self.assertEqual(g_element, expected_value)

    def test_add_edge(self):
        g = Graph()
        g.add_node("new")
        g.add_node("node")
        g.add_edge("new", "node")
        test_list = [(g.representation, {"new": [("new", "node", 999)], "node": []}),
                     (g.dist, {"new": {"new": 999, "node": 999}, "node": {"new": 999, "node": 999}}),
                     (g.nb_nodes, 2),
                     (g.nb_edges, 1)]
        for g_element, expected_value in test_list:
            with self.subTest():
                self.assertEqual(g_element, expected_value)

    def test_add_the_same_edge_twice(self):
        g = Graph()
        g.add_node("new")
        g.add_node("node")
        g.add_edge("new", "node")
        g.add_edge("new", "node")
        test_list = [(g.representation, {"new": [("new", "node", 999)], "node": []}),
                     (g.dist, {"new": {"new": 999, "node": 999}, "node": {"new": 999, "node": 999}}),
                     (g.nb_nodes, 2),
                     (g.nb_edges, 1)]
        for g_element, expected_value in test_list:
            with self.subTest():
                self.assertEqual(g_element, expected_value)

    def test_add_two_edges(self):
        g = Graph()
        g.add_node("new")
        g.add_node("node")
        g.add_node("test")
        g.add_edge("new", "node")
        g.add_edge("node", "test", 45)
        test_list = [(g.representation, {"new": [("new", "node", 999)], "node": [("node", "test", 45)], "test": []}),
                     (g.dist, {"new": {"new": 999, "node": 999, "test": 999},
                               "node": {"new": 999, "node": 999, "test": 45},
                               "test": {"new": 999, "node": 999, "test": 999}}),
                     (g.nb_nodes, 3),
                     (g.nb_edges, 2)]
        for g_element, expected_value in test_list:
            with self.subTest():
                self.assertEqual(g_element, expected_value)

    def test_node_list(self):
        g = Graph()
        g.add_node("new")
        g.add_node("node")
        g.add_node("test")
        self.assertEqual(["new", "node", "test"], g.node_list())

    def test_node_list_empty(self):
        g = Graph()
        self.assertEqual([], g.node_list())

    def test_get_in_neighbors_empty_graph(self):
        g = Graph()
        with self.assertRaises(IndexError) as context:
            g.get_in_neighbors("test")
            self.assertTrue(context.exception)

    def test_get_in_neighbors(self):
        g = Graph()
        g.add_node("new")
        g.add_node("node")
        g.add_node("test")
        g.add_edge("new", "node")
        g.add_edge("node", "test", 45)
        neighbors = g.get_in_neighbors("node")
        self.assertEqual(neighbors, ["new"])

    def test_get_in_neighbors_unknown_key(self):
        g = Graph()
        g.add_node("new")
        g.add_node("node")
        g.add_node("test")
        g.add_edge("new", "node")
        g.add_edge("node", "test", 45)
        with self.assertRaises(IndexError) as context:
            g.get_in_neighbors("blip")
            self.assertTrue(context.exception)

    def test_get_out_neighbors_empty_graph(self):
        g = Graph()
        with self.assertRaises(IndexError) as context:
            g.get_out_neighbors("test")
            self.assertTrue(context.exception)

    def test_get_out_neighbors(self):
        g = Graph()
        g.add_node("new")
        g.add_node("node")
        g.add_node("test")
        g.add_edge("new", "node")
        g.add_edge("node", "test", 45)
        neighbors = g.get_out_neighbors("new")
        self.assertEqual(neighbors, ["node"])

    def test_get_out_neighbors_unknown_key(self):
        g = Graph()
        g.add_node("new")
        g.add_node("node")
        g.add_node("test")
        g.add_edge("new", "node")
        g.add_edge("node", "test", 45)
        with self.assertRaises(IndexError) as context:
            g.get_out_neighbors("blip")
            self.assertTrue(context.exception)

    def test_in_degree(self):
        g = Graph()
        g.add_node("new")
        g.add_node("node")
        g.add_node("test")
        g.add_edge("new", "node")
        g.add_edge("node", "test", 45)
        deg = g.in_degree("node")
        self.assertEqual(deg, 1)

    def test_in_degree_unknown_key(self):
        g = Graph()
        g.add_node("new")
        g.add_node("node")
        g.add_node("test")
        g.add_edge("new", "node")
        g.add_edge("node", "test", 45)
        with self.assertRaises(IndexError) as context:
            g.in_degree("blip")
            self.assertTrue(context.exception)

    def test_out_degree(self):
        g = Graph()
        g.add_node("new")
        g.add_node("node")
        g.add_node("test")
        g.add_edge("new", "node")
        g.add_edge("node", "test", 45)
        deg = g.out_degree("new")
        self.assertEqual(deg, 1)

    def test_out_degree_unknown_key(self):
        g = Graph()
        g.add_node("new")
        g.add_node("node")
        g.add_node("test")
        g.add_edge("new", "node")
        g.add_edge("node", "test", 45)
        with self.assertRaises(IndexError) as context:
            g.out_degree("blip")
            self.assertTrue(context.exception)

    def test_edge_list_empty_graph(self):
        g = Graph()
        edges = g.edge_list()
        self.assertEqual(edges, [])

    def test_edge_list(self):
        g = Graph()
        g.add_node("new")
        g.add_node("node")
        g.add_node("test")
        g.add_edge("new", "node")
        g.add_edge("node", "test", 45)
        edges = g.edge_list()
        self.assertEqual(edges, [("new", "node", 999), ("node", "test", 45)])

    def test_get_dist_matrix_empty_graph(self):
        g = Graph()
        mat = g.get_dist_matrix()
        self.assertEqual(mat, {})

    def test_get_dist_matrix(self):
        g = Graph()
        g.add_node("new")
        g.add_node("node")
        g.add_node("test")
        g.add_edge("new", "node")
        g.add_edge("node", "test", 45)
        mat = g.get_dist_matrix()
        self.assertEqual(mat, {"new": {"new": 999, "node": 999, "test": 999},
                               "node": {"new": 999, "node": 999, "test": 45},
                               "test": {"new": 999, "node": 999, "test": 999}})

    def test_str(self):
        g = Graph()
        out = io.StringIO()
        sys.stdout = out
        print(g)
        self.assertEqual(out.getvalue(), "{}\n")

    def test_str_full(self):
        g = Graph()
        g.add_node("new")
        g.add_node("node")
        g.add_node("test")
        g.add_edge("new", "node")
        g.add_edge("node", "test", 45)
        out = io.StringIO()
        sys.stdout = out
        print(g)
        self.assertEqual(out.getvalue(), "{'new': [('new', 'node', 999)], 'node': [('node', 'test', 45)], 'test': []}\n")


if __name__ == '__main__':
    unittest.main()
