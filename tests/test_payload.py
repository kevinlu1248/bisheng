import pytest
from src.backend.bisheng.utils.payload import extract_input_variables, get_root_node, build_json

def test_extract_input_variables():
    nodes = [
        {'data': {'node': {'template': {'_type': 'prompt', 'template': {'value': 'Hello {name}'}, 'input_variables': {}}}}},
        {'data': {'node': {'template': {'_type': 'few_shot', 'prefix': {'value': 'Hello '}, 'suffix': {'value': '{name}'}, 'input_variables': {}}}}},
        {'data': {'node': {'template': {'_type': 'other', 'input_variables': {}}}}}
    ]
    result = extract_input_variables(nodes)
    assert result[0]['data']['node']['template']['input_variables']['value'] == ['name']
    assert result[1]['data']['node']['template']['input_variables']['value'] == ['name']
    assert result[2]['data']['node']['template']['input_variables']['value'] == []

def test_get_root_node():
    class Node:
        def __init__(self, base_type=None):
            self.base_type = base_type
            self.edges = []

    class Edge:
        def __init__(self, source):
            self.source = source

    graph = Node('inputOutput')
    graph.edges = [Edge(Node()), Edge(Node('inputOutput'))]
    result = get_root_node(graph)
    assert len(result) == 2

def test_build_json():
    class Node:
        def __init__(self, data):
            self.data = data
            self.edges = []

    class Graph:
        def get_nodes_with_target(self, target):
            return [Node({'node': {'template': {'_type': 'prompt', 'template': {'value': 'Hello {name}', 'type': 'string', 'required': True, 'list': False}}}})]

    root = Node({'node': {'template': {'_type': 'prompt', 'template': {'value': 'Hello {name}', 'type': 'string', 'required': True, 'list': False}}}})
    graph = Graph()
    result = build_json(root, graph)
    assert result == {'_type': 'prompt', 'template': {'value': 'Hello {name}', 'type': 'string', 'required': True, 'list': False}}
