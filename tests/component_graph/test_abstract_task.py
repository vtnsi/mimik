from unittest import TestCase
from mimik.component_graph.abstract_task import AbstractTask


class TestTask(TestCase):
    """
    A class to test the Task class
    """

    def setUp(self):
        """
        Tests the Task's __init__ function
        """
        name = "test_task"
        task_dict = {"probability": 1.0}
        self.test_task = AbstractTask(name, task_dict)

    def test_init(self):
        """
        Tests the init function of AbstractTask
        """
        self.assertEqual(self.test_task.task_name, "test_task")
        self.assertEqual(self.test_task.probability, 1.0)

    def test_forward(self):
        """
        Tests the forward function of AbstractTask
        """
        self.assertEqual(self.test_task.forward(), 1.0)
