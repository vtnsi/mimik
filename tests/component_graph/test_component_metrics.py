import builtins
import os
import pytest
from unittest.mock import MagicMock
from mimik.component_graph.component_graph import ComponentGraph
from mimik.component_graph.component_graph_metrics import ComponentGraphMetrics
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
        component_graph = ComponentGraph(working_dir=os.path.join(".", "tests"))
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

    @pytest.fixture
    def test_metrics(self, test_component_capabilities):
        """
        Creates a ComponentGraphMetrics object based on the ComponetGraphCapabilities

        Args:
            test_component_capabilities (ComponetGraphCapabilities): The test_graph returned from the fixture

        Returns:
            ComponentGraphMetrics: A ComponentGraphMetrics object to be used for testing
        """
        return ComponentGraphMetrics(test_component_capabilities)

    def test_print_probability_of_paths(self, test_component_graph, test_metrics, monkeypatch):
        """
        Tests the ComponentGraphMetrics's print_probability_of_paths method

        Args:
            test_component_graph (ComponentGraph): The test_component_graph returned from the fixture
            test_metrics (ComponentGraphMetrics): The test_metrics returned from the fixture
            monkeypatch (pytest.monkeypatch): A monkeypatch object to patch functions
        """
        def mock_stdout(print_string):
            assert print_string.split('\n')[0] == "Path: Test_Component_1, Test_Component_2, Test_Component_3"
        monkeypatch.setattr(builtins, 'print', mock_stdout)
        test_metrics.print_probability_of_paths()

        test_component_graph.add_new_component("Test_Component_2_2",  ["Test_Component_3"], ["Test_Component_1"], {"task": "Test_Task_2", "task_arguments": {"probability": 1.0}})
        test_capabilities = ComponentGraphCapabilities(test_component_graph)
        test_capabilities.monte_carlo_simulation(10)
        test_metrics = ComponentGraphMetrics(test_capabilities)
        def mock_stdout(print_string):
            assert print_string.split('\n')[0] == "Path: Test_Component_1, Test_Component_2_2, Test_Component_3"
        monkeypatch.setattr(builtins, 'print', mock_stdout)
        test_metrics.print_probability_of_paths(selected_component="Test_Component_2_2")

        test_component_graph.add_new_component("Bad_Component",  ["Test_Component_3"], ["Test_Component_1"], {"task": "Test_Task_2", "task_arguments": {"probability": 0.2}})
        test_component_graph.nodes["Test_Component_2"]["component"].task.probability = 0.3
        test_capabilities = ComponentGraphCapabilities(test_component_graph)
        test_capabilities.monte_carlo_simulation(10)
        test_metrics = ComponentGraphMetrics(test_capabilities)
        test_metrics.print_probability_of_paths(print_top_n_paths=1)

    def test_proportion_complete(self, test_metrics):
        """
        Tests the ComponentGraphMetrics's proportion_complete method
T
        Args:
            test_metrics (ComponentGraphMetrics): The test_metrics returned from the fixture
        """
        proportion_complete = round(test_metrics.proportion_complete(["Test_Component_1", "Test_Component_2", "Test_Component_3"]), 2)
        assert 0.5 <= proportion_complete <= 0.9

    def test_average_num_success(self, test_metrics):
        """
        Tests the ComponentGraphMetrics's average_num_success method

        Args:
            test_metrics (ComponentGraphMetrics): The test_metrics returned from the fixture
        """
        average_num_successes = round(test_metrics.average_num_success(["Test_Component_1", "Test_Component_2", "Test_Component_3"]), 2)
        assert 2.2 <= average_num_successes <= 2.8

    def test_calculate_variance(self, test_metrics):
        """
        Tests the ComponentGraphMetrics's calculate_variance method

        Args:
            test_metrics (ComponentGraphMetrics): The test_metrics returned from the fixture
        """
        variance = round(test_metrics.calculate_variance(["Test_Component_1", "Test_Component_2", "Test_Component_3"]), 2)
        assert 0.05 <= variance <= 1.5

    def test_plot_MC_distribution(self, test_metrics, mocker):
        """
        Tests the ComponentGraphMetrics's plot_MC_distribution method

        Args:
            test_metrics (ComponentGraphMetrics): The test_metrics returned from the fixture
            mocker (pytest-mock): A mocker object to create mocks
        """
        mocker.patch("matplotlib.pyplot.show")
        mock_ax = MagicMock()
        mocker.patch("matplotlib.pyplot.subplots", return_value=(MagicMock(), mock_ax))
        mock_ax.hist = MagicMock()
        mock_ax.set_xlabel = MagicMock()
        mock_ax.set_ylabel = MagicMock()
        mock_ax.set_xlim = MagicMock()
        mock_ax.set_title = MagicMock()
        test_metrics.plot_MC_distribution(
            ["Test_Component_1", "Test_Component_2", "Test_Component_3"]
        )
        mock_ax.set_title.assert_called_once_with("Distribution of Successful Events")

    def test_compute_node_centrality(self, test_metrics):
        """
        Tests the ComponentGraphMetrics's compute_node_centrality method

        Args:
            test_metrics (ComponentGraphMetrics): The test_metrics returned from the fixture
        """
        test_metrics.capabilities.graph.add_new_component("Test_Component_2_2",  ["Test_Component_3"], ["Test_Component_1"], {"task": "Test_Task_2", "task_arguments": {"probability": 0.2}})
        return_centrality = test_metrics.compute_node_centrality()
        assert return_centrality[0][0] == (2.0, "Test_Component_3")
        assert return_centrality[0][1] == (1.0, "Test_Component_2_2")
        assert return_centrality[0][2] == (1.0, "Test_Component_2")
        assert return_centrality[1][0] == (2.0, "Test_Component_1")
        assert return_centrality[1][1] == (1.0, "Test_Component_2_2")
        assert return_centrality[1][2] == (1.0, "Test_Component_2")
