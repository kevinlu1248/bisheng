import unittest
from unittest.mock import MagicMock

from src.backend.bisheng.utils.payload import (build_json,
                                               extract_input_variables,
                                               get_root_node)


class TestExtractInputVariables(unittest.TestCase):
    def test_extract_with_prompt_type(self):
        nodes = [{'data': {'node': {'template': {'_type': 'prompt', 'template': {'value': '{var1} and {var2}'}, 'input_variables': {'value': []}}}}}]
        expected = [{'data': {'node': {'template': {'_type': 'prompt', 'template': {'value': '{var1} and {var2}'}, 'input_variables': {'value': ['var1', 'var2']}}}}}]
        self.assertEqual(extract_input_variables(nodes), expected)

    def test_extract_with_few_shot_type(self):
        nodes = [{'data': {'node': {'template': {'_type': 'few_shot', 'prefix': {'value': '{varA}'}, 'suffix': {'value': '{varB}'}, 'input_variables': {'value': []}}}}}]
        expected = [{'data': {'node': {'template': {'_type': 'few_shot', 'prefix': {'value': '{varA}'}, 'suffix': {'value': '{varB}'}, 'input_variables': {'value': ['varA', 'varB']}}}}}]
        self.assertEqual(extract_input_variables(nodes), expected)

    def test_extract_with_no_variables(self):
        nodes = [{'data': {'node': {'template': {'_type': 'prompt', 'template': {'value': 'no variables here'}, 'input_variables': {'value': []}}}}}]
        expected = [{'data': {'node': {'template': {'_type': 'prompt', 'template': {'value': 'no variables here'}, 'input_variables': {'value': []}}}}}]
        self.assertEqual(extract_input_variables(nodes), expected)

class TestGetRootNode(unittest.TestCase):
    def setUp(self):
        self.mock_graph = MagicMock()
        self.mock_graph.nodes = []
        self.mock_graph.edges = []

    def test_single_node_graph(self):
        self.mock_graph.nodes = ['node1']
        self.assertEqual(get_root_node(self.mock_graph), 'node1')

    def test_graph_with_clear_root(self):
        self.mock_graph.nodes = ['node1', 'node2']
        self.mock_graph.edges = [MagicMock(source='node2', target='node1')]
        self.assertEqual(get_root_node(self.mock_graph), 'node2')

    def test_graph_with_input_output_base_type(self):
        self.mock_graph.nodes = ['node1', 'node2']
        self.mock_graph.edges = [MagicMock(source='node1', target='node2', source_base_type='inputOutput')]
        self.assertEqual(get_root_node(self.mock_graph), 'node1')

class TestBuildJson(unittest.TestCase):
    def setUp(self):
        self.mock_graph = MagicMock()
        self.mock_root = MagicMock()

    def test_build_json_single_child(self):
        self.mock_root.data = {'node': {'template': {'_type': 'prompt', 'template': {'value': 'test'}, 'input_variables': {'value': []}}}}
        self.mock_graph.get_nodes_with_target.return_value = [self.mock_root]
        expected = {'_type': 'prompt', 'template': {'value': 'test'}, 'input_variables': {'value': []}}
        self.assertEqual(build_json(self.mock_root, self.mock_graph), expected)

    def test_build_json_with_missing_required_child(self):
        self.mock_root.data = {'node': {'template': {'_type': 'dict', 'required': True}}}
        self.mock_graph.get_nodes_with_target.return_value = []
        with self.assertRaises(ValueError):
            build_json(self.mock_root, self.mock_graph)

    def test_build_json_complex_structure(self):
        self.mock_root.data = {'node': {'template': {'_type': 'dict', 'list': True, 'children': {'_type': 'prompt', 'template': {'value': 'child'}}}}}
        child_mock = MagicMock()
        child_mock.data = {'node': {'template': {'_type': 'prompt', 'template': {'value': 'child'}}}}
        self.mock_graph.get_nodes_with_target.return_value = [child_mock]
        self.mock_graph.get_children_by_node_type.return_value = [child_mock]
        expected = {'_type': 'dict', 'list': True, 'children': [{'_type': 'prompt', 'template': {'value': 'child'}}]}
        self.assertEqual(build_json(self.mock_root, self.mock_graph), expected)

if __name__ == '__main__':
    unittest.main()
