import unittest
from bisheng.utils.payload import extract_input_variables, get_root_node, build_json


class TestPayload(unittest.TestCase):
    def test_extract_input_variables(self):
        # Test case: 'prompt' type with input_variables field
        nodes = [{'data': {'node': {'template': {'_type': 'prompt', 'template': {'value': 'Hello {name}'}, 'input_variables': {}}}}}]
        result = extract_input_variables(nodes)
        self.assertEqual(result[0]['data']['node']['template']['input_variables']['value'], ['name'])
    
        # Test case: 'few_shot' type with input_variables field
        nodes = [{'data': {'node': {'template': {'_type': 'few_shot', 'prefix': {'value': 'Hello '}, 'suffix': {'value': '{name}'}, 'input_variables': {}}}}}]
        result = extract_input_variables(nodes)
        self.assertEqual(result[0]['data']['node']['template']['input_variables']['value'], ['name'])
    
        # Test case: other type with input_variables field
        nodes = [{'data': {'node': {'template': {'_type': 'other', 'input_variables': {}}}}}]
        result = extract_input_variables(nodes)
        self.assertEqual(result[0]['data']['node']['template']['input_variables']['value'], [])
    
        # Test case: 'prompt' type without input_variables field
        nodes = [{'data': {'node': {'template': {'_type': 'prompt', 'template': {'value': 'Hello {name}'}}}}}]
        result = extract_input_variables(nodes)
        self.assertEqual(result[0]['data']['node']['template'].get('input_variables'), None)
    
        # Test case: 'few_shot' type without input_variables field
        nodes = [{'data': {'node': {'template': {'_type': 'few_shot', 'prefix': {'value': 'Hello '}, 'suffix': {'value': '{name}'}}}}}]
        result = extract_input_variables(nodes)
        self.assertEqual(result[0]['data']['node']['template'].get('input_variables'), None)
    
        # Test case: other type without input_variables field
        nodes = [{'data': {'node': {'template': {'_type': 'other'}}}}]
        result = extract_input_variables(nodes)
        self.assertEqual(result[0]['data']['node']['template'].get('input_variables'), None)

    def test_get_root_node(self):
        class Node:
            def __init__(self, base_type):
                self.base_type = base_type
        class Edge:
            def __init__(self, source):
                self.source = source
        class Graph:
            def __init__(self, nodes, edges):
                self.nodes = nodes
                self.edges = edges
        graph1 = Graph([Node('inputOutput')], [Edge(Node('inputOutput'))])
        graph2 = Graph([Node('other')], [Edge(Node('other'))])
        self.assertEqual(get_root_node(graph1), {Node('inputOutput')})
        self.assertEqual(get_root_node(graph2), {Node('other')})

    def test_build_json(self):
        class Node:
            def __init__(self, data, edges=[]):
                self.data = data
                self.edges = edges
        class Graph:
            def __init__(self, nodes):
                self.nodes = nodes
            def get_nodes_with_target(self, target):
                return [node for node in self.nodes if node.data == target.data]
            def get_children_by_node_type(self, node, node_type):
                return [child for child in node.edges if child.data['node']['template']['type'] == node_type]
        root = Node({'node': {'template': {'_type': 'prompt', 'template': {'value': 'Hello {name}', 'type': 'string', 'required': True, 'list': False}}}})
        graph = Graph([root])
        result = build_json(root, graph)
        self.assertEqual(result, {'_type': 'prompt', 'template': 'Hello {name}'})
