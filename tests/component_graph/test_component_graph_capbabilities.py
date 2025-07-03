import builtins
import os
import pytest
from mimik.component_graph.component_graph import ComponentGraph
from mimik.component_graph.component_graph_capabilities import ComponentGraphCapabilities


class TestComponentMetrics():
    """
    A class for testing the ComponentMetrics class
    """

    @pytest.fixture
    def test_component_graph(self):
        """
        Creates the ComponetGraph object

        Returns:
            ComponentGraph: A ComponentGraph object to be used for testing
        """
        component_graph = ComponentGraph(working_dir=os.path.join(".", "tests"), silent=True)
        component_graph.load_killweb_from_config_file(os.path.join(".", "tests", "test_configs", "test_json.json"))
        return component_graph

    @pytest.fixture
    def test_component_capabilities(self, test_component_graph):
        """
        Creates the ComponetGraphCapabilities object

        Args:
            test_component_graph (ComponentGraph): The test_graph returned from the fixture        

        Returns:
            ComponetGraphCapabilities: A ComponetGraphCapabilities object to be used for testing
        """
        capabilities = ComponentGraphCapabilities(test_component_graph)
        capabilities.monte_carlo_simulation(100)
        return capabilities

    def test_print_all_paths(self, test_component_capabilities, monkeypatch):
        """
        Tests the ComponentGraphMetrics's print_all_paths method

        Args:
            test_component_capabilities (ComponentGraphMetrics): The test_component_capabilities returned from the fixture
            monkeypatch (pytest.monkeypatch): A monkeypatch object to patch functions
        """
        def mock_stdout(print_string):
            assert (print_string == "Test_Component_1, Test_Component_2, Test_Component_3") or (print_string == "\nThere are 1 paths through the killweb")
        monkeypatch.setattr(builtins, 'print', mock_stdout)
        test_component_capabilities.print_all_paths()
