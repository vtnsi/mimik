from mimik.component_graph.abstract_task import AbstractTask


class Find(AbstractTask):
    """
    Class for Find task
    """

    def __init__(self, arguments: dict):
        """
        Initialize custom Find class

        Parameters:
            arguments (dict): A dictionary of all the arguments

        Required Inputs:
            I - number of valid targets
            J - number of possible targets
        """
        super().__init__("Find", arguments)
        self.I = arguments["I"]
        self.J = arguments["J"]

    def forward(self):
        return self.I / self.J
