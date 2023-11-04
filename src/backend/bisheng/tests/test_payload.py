import unittest
from bisheng.utils.payload import extract_input_variables, get_root_node, build_json

class TestPayloadFunctions(unittest.TestCase):

    def test_extract_input_variables(self):
        nodes = [
            {
                'data': {
                    'node': {
                        'template': {
                            '_type': 'prompt',
                            'template': {'value': 'Hello {name}'},
                            'input_variables': {}
                        }
                    }
                }
            },
            {
                'data': {
                    'node': {
                        'template': {
                            '_type': 'few_shot',
                            'prefix': {'value': 'Hello {name}'},
                            'suffix': {'value': ', how are you?'},
                            'input_variables': {}
                        }
                    }
                }
            },
            {
                'data': {
                    'node': {
                        'template': {
                            '_type': 'other',
                            'input_variables': {}
                        }
                    }
                }
            }
        ]
        result = extract_input_variables(nodes)
        self.assertEqual(result[0]['data']['node']['template']['input_variables']['value'], ['name'])
        self.assertEqual(result[1]['data']['node']['template']['input_variables']['value'], ['name'])
        self.assertEqual(result[2]['data']['node']['template']['input_variables']['value'], [])

    def test_get_root_node(self):
        class Node:
            def __init__(self, base_type=None):
                self.base_type = base_type
                self.edges = []

        class Edge:
            def __init__(self, source):
                self.source = source

        graph = Node('inputOutput')
        graph.edges.append(Edge(Node()))
        result = get_root_node(graph)
        self.assertEqual(result, {graph})

    def test_build_json(self):
        class Node:
            def __init__(self, data=None, edges=None, node_type=None):
                self.data = data if data else {}
                self.edges = edges if edges else []
                self.node_type = node_type

        class Graph:
            def get_nodes_with_target(self, target):
                return [Node({'node': {'template': {'_type': 'prompt', 'template': {'value': 'Hello {name}'}}}})]

            def get_children_by_node_type(self, node, node_type):
                return []

        root = Node({'node': {'template': {'_type': 'prompt', 'template': {'value': 'Hello {name}'}}}})
        graph = Graph()
        result = build_json(root, graph)
        self.assertEqual(result, {'_type': 'prompt', 'template': {'value': 'Hello {name}'}})

if __name__ == '__main__':
    unittest.main()
