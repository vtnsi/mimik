from unittest import TestCase
from mimik.component_graph.component import Component
from mimik.component_graph.abstract_task import AbstractTask



class TestComponent(TestCase):
    """
    A class for testing the Component class
    """

    def setUp(self):
        """
        Sets up the test component object
        """
        self.test_component = Component(
            "test_component",
            ["test_component_2"]
        )
        self.test_component.add_task(AbstractTask("test_task", {"probability": 1.0}))
        self.test_component.add_system_name("test_system")

    def test_init(self):
        """
        Tests the Component's __init__ method
        """
        self.assertEqual(self.test_component.full_name, "test_component")
        self.assertEqual(self.test_component.task.task_name, "test_task")
        self.assertEqual(self.test_component.task.probability, 1.0)
        self.assertEqual(
            self.test_component.connected_component_names, ["test_component_2"]
        )
        self.assertEqual(self.test_component.system_name, "test_system")
