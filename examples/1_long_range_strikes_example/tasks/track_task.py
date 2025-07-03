from mimik.component_graph.abstract_task import AbstractTask
from scipy.stats import gamma


class Track(AbstractTask):
    """
    Class for Track event
    """

    def __init__(self, arguments: dict):
        """
        Initialize custom Track class

        Parameters:
            task_name (str): The name of the task
            arguments (dict): A dictionary of all the arguments
        Required Inputs:
            alpha - shape parameter for gamma distrubiton
            beta - rate parameter for gamma distribution
            tau - minimum time to track target
        """
        super().__init__("Track", arguments)
        self.alpha = arguments["alpha_track"]
        self.beta = arguments["beta_track"]
        self.tau = arguments["tau"]

    def forward(self):
        return 1 - gamma.cdf(self.tau, self.alpha, scale=1 / self.beta)
