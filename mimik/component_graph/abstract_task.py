from abc import ABC


class AbstractTask(ABC):
    def __init__(self, task_name: str, arguments: dict):
        """
        A constructor for the abstract Task class

        Parameters:
            task_name (str): The name of the task to complete
            arguments (dict): The arguments to find probability in if static probability is being used
        """
        self.task_name = task_name
        self.task_arguments = arguments
        if "probability" in arguments.keys():
            self.probability = arguments["probability"]

    def forward(self):
        """
        The default forward function of the task

        Returns:
            The static probability associated with the task
        """
        return self.probability
