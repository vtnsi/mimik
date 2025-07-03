import pytest
import os
from mimik.component_graph.task_factory import TaskFactory

class TestTaskFactory:
    """
    A class to test the TaskFactory class
    """

    @pytest.fixture
    def test_task_factory(self):
        """
        Creates a TaskFactory object

        Returns:
            TaskFactory: The test TaskFactory object
        """
        return TaskFactory(os.path.join(os.getcwd(), "tests", "test_tasks"), False)

    def test_create_task(self, test_task_factory):
        found_task = test_task_factory.create_task("Random", {'x': 1, 'y': 2})
        not_found_task = test_task_factory.create_task("Random", {'probability': 1.0})
        assert found_task.forward() == 3
        assert not_found_task.forward() == 1.0
        with pytest.raises(KeyError):
            error_task = test_task_factory.create_task("Random", {'bad_parameter': "ABC123"})