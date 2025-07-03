from mimik.component_graph.abstract_task import AbstractTask


class Random(AbstractTask):
    """
    Class for Test task
    """

    def __init__(self, arguments: dict):
        """
        Initialize custom RandomTask class

        Parameters:
            arguments (dict): A dictionary of all the arguments

        Required Inputs:
            x - Test input 1
            y - Test input 2
        """
        super().__init__("Random", arguments)
        self.x = arguments["x"]
        self.y = arguments["y"]

    def forward(self):
        return self.x + self.y
