from mimik.component_graph.abstract_task import AbstractTask
from scipy.stats import beta


class Engage(AbstractTask):
    """
    Class for Engage task
    """

    def __init__(self, arguments: dict):
        """
        Initialize custom Engage class

        Parameters:
            arguments (dict): A dictionary of all the arguments

        Required Inputs:
            alpha - shape parameter for gamma distrubiton
            beta - rate parameter for gamma distribution
        """
        super().__init__("Engage", arguments)
        self.alpha = arguments["alpha_engage"]
        self.beta = arguments["beta_engage"]

    def forward(self):
        return beta.rvs(self.alpha, self.beta)
