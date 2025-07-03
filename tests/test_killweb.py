import os
import builtins
import pytest
import networkx as nx
from unittest.mock import MagicMock
from mimik.killweb import Killweb


class TestKillweb:
    """
    A class for testing the Killweb class
    """

    @pytest.fixture
    def test_killweb(self, mocker) -> Killweb:
        """
        Tests the Killweb's __init__ function

        Returns:
            Killweb: A killweb object to be used for testing
        """
        mocker.patch("matplotlib.pyplot.show")
        killweb = Killweb(
            working_dir="tests",
            config_file=os.path.join("tests", "test_configs", "test_json.json"),
            silent=False
        )
        killweb.monte_carlo_on_paths(100)
        return killweb

    def test_create_component_networkx_visualization(self, test_killweb: Killweb, mocker):
        """
        Test the Killweb's create_component_networkx_visualization method

        Args:
            test_killweb (Killweb): The test killweb from the fixture
            mocker (pytest-mock): An object to create mocks by patching functions
        """
        mocker.patch("mimik.component_graph.component_graph.plt.show")
        mocker.patch("mimik.component_graph.component_graph.plt.subplots", return_value=(MagicMock(), MagicMock()))
        mock_draw = MagicMock()
        mock_to_agraph = MagicMock()
        mock_to_agraph = mocker.patch("networkx.nx_agraph.to_agraph")
        mock_to_agraph.return_value.draw = mock_draw
        test_killweb.create_component_networkx_visualization()
        mock_draw.assert_called_with(
            os.path.join("tests", "output", "component_networkx_model.png"), prog="neato"
        )

    def test_add_new_component(self, test_killweb: Killweb):
        """
        Test the Killweb's add_new_component method

        Args:
            test_killweb (Killweb): The test killweb from the fixture
        """
        test_killweb.add_new_component("Test_Component_2_2",  ["Test_Component_3"], ["Test_Component_1"], {"task": "Test_Task_2", "task_arguments": {"probability": 0.9}})
        assert len(test_killweb.component_graph.nodes) == 4
        assert test_killweb.component_graph.nodes["Test_Component_1"]["component"]
        assert len(nx.descendants(test_killweb.component_graph, "Test_Component_1")) == 3
        assert len(nx.descendants(test_killweb.component_graph, "Test_Component_2")) == 1
        assert len(nx.descendants(test_killweb.component_graph, "Test_Component_2_2")) == 1
        assert len(nx.ancestors(test_killweb.component_graph, "Test_Component_3")) == 3

    def test_add_new_edge(self, test_killweb: Killweb):
        """
        Test the Killweb's add_new_edge method

        Args:
            test_killweb (Killweb): The test killweb from the fixture
        """
        test_killweb.add_new_component("Test_Component_2_2",  ["Test_Component_3"], ["Test_Component_1"], {"task": "Test_Task_2", "task_arguments": {"probability": 0.9}})
        test_killweb.add_new_component("Test_Component_3_2", [], ["Test_Component_2"], {"task": "Test_Task_3", "task_arguments": {"probability": 0.9}})
        assert len(nx.ancestors(test_killweb.component_graph, "Test_Component_3_2")) == 2
        test_killweb.add_new_edge("Test_Component_2_2", "Test_Component_3_2")
        assert len(nx.ancestors(test_killweb.component_graph, "Test_Component_3_2")) == 3

    def test_remove_component(self, test_killweb: Killweb):
        """
        Tests the Killweb's remove_component method

        Args:
            test_killweb (Killweb): The test killweb from the fixture
        """
        test_killweb.remove_component("Test_Component_3")
        assert len(test_killweb.component_graph.nodes()) == 2
        assert len(nx.descendants(test_killweb.component_graph, "Test_Component_2")) == 0

    def test_remove_edge(self, test_killweb: Killweb):
        """
        Tests the Killweb's remove_edge method

        Args:
            test_killweb (Killweb): The test killweb from the fixture
        """
        test_killweb.remove_edge(from_component_name="Test_Component_2", to_component_name="Test_Component_3")
        assert len(test_killweb.component_graph.edges()) == 1
        assert len(nx.descendants(test_killweb.component_graph, "Test_Component_2")) == 0

    def test_print_nodes(self, test_killweb: Killweb, monkeypatch):
        """
        Tests the Killweb's print_nodes method

        Args:
            test_killweb (Killweb): The test killweb from the fixture
            monkeypatch (pytest.monkeypatch): An object to patch functions by overwriting them
        """
        def mock_stdout(print_string):
            assert (str(print_string) == "['Test_Component_1', 'Test_Component_2', 'Test_Component_3']")
        monkeypatch.setattr(builtins, 'print', mock_stdout)
        test_killweb.print_nodes()

    def test_print_edges(self, test_killweb: Killweb, monkeypatch):
        """
        Tests the Killweb's print_edges method

        Args:
            test_killweb (Killweb): The test killweb from the fixture
            monkeypatch (pytest.monkeypatch): An object to patch functions by overwriting them
        """
        def mock_stdout(print_string):
            assert (str(print_string) == "[('Test_Component_1', 'Test_Component_2'), ('Test_Component_2', 'Test_Component_3')]")
        monkeypatch.setattr(builtins, 'print', mock_stdout)
        test_killweb.print_edges()

    def test_print_all_paths_in_killweb(self, test_killweb: Killweb, monkeypatch):
        """
        Test the Killweb's print_all_paths_in_killweb method

        Args:
            test_killweb (Killweb): The test killweb from the fixture
            monkeypatch (pytest.monkeypatch): An object to patch functions by overwriting them
        """
        def mock_stdout(print_string):
            assert (print_string == "Test_Component_1, Test_Component_2, Test_Component_3") or (print_string == "\nThere are 1 paths through the killweb")
        monkeypatch.setattr(builtins, 'print', mock_stdout)
        test_killweb.print_all_paths_in_killweb()

    def test_print_probabilities_of_paths(self, test_killweb: Killweb, monkeypatch):
        """
        Test the Killweb's print_probability_of_paths method

        Args:
            test_killweb (Killweb): The test killweb from the fixture
            monkeypatch (pytest.monkeypatch): An object to patch functions by overwriting them
        """
        def mock_stdout(print_string):
            assert print_string.split('\n')[0] == "Path: Test_Component_1, Test_Component_2, Test_Component_3"
        monkeypatch.setattr(builtins, 'print', mock_stdout)
        test_killweb.print_probabilities_of_paths()

        test_killweb.add_new_component("Test_Component_2_2",  ["Test_Component_3"], ["Test_Component_1"], {"task": "Test_Task_2", "task_arguments": {"probability": 1.0}, "system_name": "Test_System_2"})
        def mock_stdout(print_string):
            assert print_string.split('\n')[0] == "Path: Test_Component_1, Test_Component_2_2, Test_Component_3"
        monkeypatch.setattr(builtins, 'print', mock_stdout)
        test_killweb.monte_carlo_on_paths(10)
        test_killweb.print_probabilities_of_paths(selected_component="Test_Component_2_2")

        test_killweb.component_graph.nodes["Test_Component_2"]["component"].task.probability = 0.3
        test_killweb.add_new_component("Bad_Component",  ["Test_Component_3"], ["Test_Component_1"], {"task": "Test_Task_2", "task_arguments": {"probability": 0.2}, "system_name": "Test_System_2"})
        test_killweb.monte_carlo_on_paths(10)
        test_killweb.print_probabilities_of_paths(amount_to_print=1)
    
    def test_print_proportion_complete(self, test_killweb: Killweb):
        """
        Test the Killweb's proportion_complete method

        Args:
            test_killweb (Killweb): The test killweb from the fixture
        """
        proportion_complete = round(test_killweb.print_proportion_complete(["Test_Component_1", "Test_Component_2", "Test_Component_3"]), 2)
        assert 0.6 <= proportion_complete <= 0.9

    def test_print_average_number_of_successes(self, test_killweb: Killweb):
        """
        Test the Killweb's print_average_number_of_successes method

        Args:
            test_killweb (Killweb): The test killweb from the fixture
        """
        average_num_successes = round(test_killweb.print_average_number_of_successes(["Test_Component_1", "Test_Component_2", "Test_Component_3"]), 2)
        assert 2.2 <= average_num_successes <= 2.8

    def test_print_variance(self, test_killweb: Killweb):
        """
        Tests the ComponentGraphMetrics's print_variance method

        Args:
            test_killweb (Killweb): The test killweb from the fixture
        """
        variance = round(test_killweb.print_variance(["Test_Component_1", "Test_Component_2", "Test_Component_3"]), 2)
        assert 0.05 <= variance <= 1.5

    def test_plot_monte_carlo_distribution(self, test_killweb: Killweb, mocker):
        """
        Test the Killweb's plot_monte_carlo_distribution method

        Args:
            test_killweb (Killweb): The test killweb from the fixture
            mocker (pytest-mock): An object to create mocks by patching functions
        """
        mocker.patch("matplotlib.pyplot.show")
        mock_ax = MagicMock()
        mocker.patch("matplotlib.pyplot.subplots", return_value=(MagicMock(), mock_ax))
        mock_ax.hist = MagicMock()
        mock_ax.set_xlabel = MagicMock()
        mock_ax.set_ylabel = MagicMock()
        mock_ax.set_xlim = MagicMock()
        mock_ax.set_title = MagicMock()
        test_killweb.plot_monte_carlo_distribution(
            ["Test_Component_1", "Test_Component_2", "Test_Component_3"]
        )
        mock_ax.set_title.assert_called_once_with("Distribution of Successful Events")

    def test_get_monte_carlo_results(self, test_killweb: Killweb):
        """
        Tests the Killweb's get_monte_carlo_results method

        Args:
            test_killweb (Killweb): _description_
        """
        outcomes, probabilities = test_killweb.get_monte_carlo_results()
        assert len(outcomes["Test_Component_1, Test_Component_2, Test_Component_3"]) == 100
        assert len(probabilities["Test_Component_1, Test_Component_2, Test_Component_3"]) == 100

    def test_calculate_node_centrality(self, test_killweb: Killweb):
        """
        Test the Killweb's calculate_node_centrality method

        Args:
            test_killweb (Killweb): The test killweb from the fixture
        """
        test_killweb.add_new_component("Test_Component_2_2",  ["Test_Component_3"], ["Test_Component_1"], {"task": "Test_Task_2", "task_arguments": {"probability": 0.2}})
        return_centrality = test_killweb.calculate_node_centrality()
        assert return_centrality[0][0] == (2.0, "Test_Component_3")
        assert return_centrality[0][1] == (1.0, "Test_Component_2_2")
        assert return_centrality[0][2] == (1.0, "Test_Component_2")
        assert return_centrality[1][0] == (2.0, "Test_Component_1")
        assert return_centrality[1][1] == (1.0, "Test_Component_2_2")
        assert return_centrality[1][2] == (1.0, "Test_Component_2")
