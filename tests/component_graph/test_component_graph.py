import os
import pytest
import json
import networkx as nx
from unittest.mock import patch, mock_open, MagicMock
from mimik.component_graph.component_graph import ComponentGraph


class TestComponentGraph():
    """
    A class for testing the ComponentGraph class
    """

    @pytest.fixture
    def test_component_graph(self) -> ComponentGraph:
        """
        Creates the ComponetGraph object

        Args:
            mocker (pytest-mock): A mocker object to create mocks

        Returns:
            ComponentGraph: A ComponentGraph object to be used for testing
        """
        component_graph = ComponentGraph(working_dir=os.path.join(".", "tests"))
        component_graph.load_killweb_from_config_file(os.path.join(".", "tests", "test_configs", "test_json.json"))
        return component_graph

    def test_get_starting_components(self, test_component_graph: ComponentGraph):
        """
        Tests the ComponentGraph's init method

        Args:
            test_component_graph (ComponentGraph): The test_component_graph returned from the fixture
        """
        start_components = test_component_graph.get_start_components()
        assert len(start_components) == 1
        start_component = test_component_graph.nodes[start_components[0]]["component"]
        assert start_component.full_name == "Test_Component_1"
        assert start_component.task.task_name == "Test_Task"
        assert start_component.connected_component_names[0] == "Test_Component_2"

    def test_get_ending_components(self, test_component_graph: ComponentGraph):
        """
        Tests the ComponentGraph's init method

        Args:
            test_component_graph (ComponentGraph): The test_component_graph returned from the fixture
        """
        end_components = test_component_graph.get_end_components()
        assert len(end_components) == 1
        end_component = test_component_graph.nodes[end_components[0]]["component"]
        assert end_component.full_name == "Test_Component_3"
        assert end_component.task.task_name == "Test_Task_3"
        assert len(end_component.connected_component_names) == 0

    def test_save_killweb_to_config_file(self, test_component_graph: ComponentGraph, monkeypatch):
        """
        Tests the ComponentGraph's save_killweb_to_config_file method

        Args:
            test_component_graph (ComponentGraph): The test_component_graph returned from the fixture
        """
        def mock_dumps(killweb_dict, file, indent):
            test_json = {
                "TestKillweb": {
                    "Test_Component_1": {
                        "attributes": {
                            "task": "Test_Task",
                            "task_arguments": {"probability": 1.0},
                            "system_name": "Test_System"
                        },
                        "connected_components": [
                            "Test_Component_2"
                        ]
                    },
                    "Test_Component_2": {
                        "attributes": {
                            "task": "Test_Task_2",
                            "task_arguments": {"probability": 0.9},
                            "system_name": "Test_System"
                        },
                        "connected_components": [
                            "Test_Component_3"
                        ]
                    },
                    "Test_Component_3": {
                        "attributes": {
                            "task": "Test_Task_3",
                            "task_arguments": {"probability": 0.8},
                            "system_name": "Test_System"
                        },
                        "connected_components": []
                    }
                }
            }
            assert test_json == killweb_dict
        monkeypatch.setattr(json, "dump", mock_dumps)
        with patch(
            "mimik.component_graph.component_graph.open",
            new=mock_open(read_data="None"),
        ) as file:
            test_component_graph.save_killweb_to_config_file("test_filename", "TestKillweb")

    def test_load_killweb_from_config_file(self, test_component_graph: ComponentGraph):
        """
        Tests the ComponentGraph's load_killweb_from_config_file method

        Args:
            test_component_graph (ComponentGraph): The test_component_graph returned from the fixture
        """
        test_component_graph.load_killweb_from_config_file(os.path.join(".", "tests", "test_configs", "test_json.json"))
        assert len(test_component_graph.nodes) == 3

    def test_add_new_component(self, test_component_graph: ComponentGraph):
        """
        Tests the ComponentGraph's add_new_component method

        Args:
            test_component_graph (ComponentGraph): The test_component_graph returned from the fixture
        """
        test_component_graph.add_new_component(
            "Test_Component_2_2",
            ["Test_Component_3"],
            ["Test_Component_1"],
            {"task": "Test_Task_2", "task_arguments": {"probability": 0.9}}
        )
        assert len(test_component_graph.nodes) == 4
        assert test_component_graph.nodes["Test_Component_1"]["component"]
        assert len(nx.descendants(test_component_graph, "Test_Component_1")) == 3
        assert len(nx.descendants(test_component_graph, "Test_Component_2")) == 1
        assert len(nx.descendants(test_component_graph, "Test_Component_2_2")) == 1
        assert len(nx.ancestors(test_component_graph, "Test_Component_3")) == 3
        
    def test_add_new_edge(self, test_component_graph: ComponentGraph):
        """
        Tests the ComponentGraph's add_new_edge method

        Args:
            test_component_graph (ComponentGraph): The test_component_graph returned from the fixture
        """
        test_component_graph.add_new_component(
            "Test_Component_2_2",
            ["Test_Component_3"],
            ["Test_Component_1"],
            {"task": "Test_Task_2", "task_arguments": {"probability": 0.9}}
        )
        test_component_graph.add_new_component(
            "Test_Component_3_2",
            [],
            ["Test_Component_2"],
            {"task": "Test_Task_3", "task_arguments": {"probability": 0.9}}
        )
        test_component_graph.add_new_edge("Test_Component_2_2", "Test_Component_3_2")
        assert len(nx.descendants(test_component_graph, "Test_Component_2_2")) == 2
        assert len(nx.ancestors(test_component_graph, "Test_Component_3_2")) == 3

    def test_remove_component(self, test_component_graph: ComponentGraph):
        """
        Tests the ComponentGraph's remove_component method

        Args:
            test_component_graph (ComponentGraph): The test_component_graph returned from the fixture
        """
        test_component_graph.remove_component("Test_Component_3")
        assert len(test_component_graph.nodes()) == 2
        assert len(nx.descendants(test_component_graph, "Test_Component_2")) == 0

    def test_remove_existing_edge(self, test_component_graph: ComponentGraph):
        """
        Tests the ComponentGraph's update_annotation method

        Args:
            test_component_graph (ComponentGraph): The test_component_graph returned from the fixture
        """
        test_component_graph.remove_existing_edge("Test_Component_2", "Test_Component_3")
        assert len(test_component_graph.edges()) == 1
        assert len(nx.descendants(test_component_graph, "Test_Component_2")) == 0

    def test_update_annotation(self, test_component_graph: ComponentGraph, mocker):
        """
        Tests the ComponentGraph's update_annotation method

        Args:
            test_component_graph (ComponentGraph): The test_component_graph returned from the fixture
            mocker (pytest-mock): A mocker object to create mocks
        """
        mocker.patch("mimik.component_graph.component_graph.plt.figure")
        mock_draw = MagicMock()
        mock_to_agraph = MagicMock()
        mock_to_agraph = mocker.patch("networkx.nx_agraph.to_agraph")
        mock_to_agraph.return_value.draw = mock_draw
        test_component_graph.networkx_visualization()

        test_component_graph.fig = MagicMock()
        mock_fig_extent = MagicMock()
        test_component_graph.fig.get_window_extent.return_value = mock_fig_extent
        mock_fig_extent.x1 = 1

        test_parameter = {"ind": [0]}
        test_component_graph.pos = {
            "Test_Component_1": (0.0, 1.1),
        }
        test_component_graph.annot = MagicMock()
        mock_annot_extent = MagicMock()
        test_component_graph.annot.get_window_extent.return_value = mock_annot_extent
        mock_annot_extent.x1 = 2
        test_component_graph.update_annotation(test_parameter)
        test_component_graph.annot.set_text.assert_called_with(
            "Component Name: Test_Component_1\nTask: Test_Task\nSystem: Test_System"
        )

    def test_hover(self, test_component_graph: ComponentGraph, mocker):
        """
        Tests the ComponentGraph's hover method

        Args:
            test_component_graph (ComponentGraph): The test_component_graph returned from the fixture
            mocker (pytest-mock): A mocker object to create mocks
        """
        mocker.patch("mimik.component_graph.component_graph.plt.figure")
        mock_draw = MagicMock()
        mock_to_agraph = MagicMock()
        mock_to_agraph = mocker.patch("networkx.nx_agraph.to_agraph")
        mock_to_agraph.return_value.draw = mock_draw
        test_component_graph.networkx_visualization()

        mock_annotation = mocker.patch("mimik.component_graph.component_graph.ComponentGraph.update_annotation")
        test_component_graph.annot = MagicMock()
        test_component_graph.annot.get_window_extent = MagicMock()
        test_component_graph.annot.get_window_extent.x1 = 2
        test_component_graph.ax = 1
        new_event = MagicMock()
        new_event.inaxes = 1
        test_component_graph.graph_nodes = MagicMock()
        test_component_graph.graph_nodes.contains.return_value = (True, 1)
        test_component_graph.fig = MagicMock()
        test_component_graph.fig.get_window_extent = MagicMock()
        test_component_graph.fig.canvas.draw_idle = MagicMock()
        test_component_graph.fig.get_window_extent.x1 = 1
        test_component_graph.hover(new_event)
        mock_annotation.assert_called_once()

        test_component_graph.graph_nodes.contains.return_value = (False, 1)
        test_component_graph.hover(new_event)
        mock_annotation.assert_called_once()

    def test_networkx_visualization(self, test_component_graph: ComponentGraph, mocker):
        """
        Tests the ComponentGraph's networkx_visualization method

        Args:
            test_component_graph (ComponentGraph): The test_component_graph returned from the fixture
            mocker (pytest-mock): A mocker object to create mocks
        """
        mocker.patch("mimik.component_graph.component_graph.plt.figure")
        mock_draw = MagicMock()
        mock_to_agraph = MagicMock()
        mock_to_agraph = mocker.patch("networkx.nx_agraph.to_agraph")
        mock_to_agraph.return_value.draw = mock_draw
        test_component_graph.networkx_visualization()
        mock_draw.assert_called_with(
            os.path.join(".", "tests", "output", "component_networkx_model.png"), prog="neato"
        )
