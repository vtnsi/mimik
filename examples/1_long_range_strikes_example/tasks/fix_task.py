from mimik.component_graph.abstract_task import AbstractTask
from scipy.stats import lognorm, beta


class Fix(AbstractTask):
    """
    Class for Fix task
    """

    def __init__(self, arguments: dict):
        """
        Initialize custom Fix class

        Parameters:
            arguments (dict): A dictionary of all the arguments
        Required Inputs:
            sigma2 - vairance for log normal
            alpha - alpha parameter for beta
        """
        super().__init__("Fix", arguments)
        self.d = arguments["d"]
        self.sigma2 = arguments["sigma2"]
        self.alpha = arguments["alpha_fix"]

    def forward(self):
        b = lognorm.rvs(self.sigma2, self.d)
        return beta.rvs(self.alpha, b)
