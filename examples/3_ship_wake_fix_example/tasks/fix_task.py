import json
import numpy as np
from pgmpy.factors.discrete import TabularCPD

from tasks.component_BN import ComponentBN
from mimik.component_graph.abstract_task import AbstractTask


class Fix(AbstractTask):
    """
    Class for Fix task
    """
    def __init__(self, arguments: dict):
        """
        Initialize custom Fix class

        Parameters:
            arguments (dict): A dictionary of all the arguments
        """
        super().__init__("Fix", arguments)
        self.bn_config_file = arguments.pop("BN_config", None)
        if self.bn_config_file is None:
            raise ValueError("Need to specify BN config file name")

        self.outcome = arguments.pop("outcome", None)
        if self.outcome is None:
            raise ValueError("Need to specify the outcome node name")

        self.condition = arguments.pop("condition", None)
        if self.condition is None:
            raise ValueError("Need to set success value of outcome node")
        self.arguments = arguments
        self._construct_bn()

    def _construct_bn(self):
        """
        Create the Bayesian Network (BN) from the config json file defined by
        `BN_config` in the arguments. The function will create the Conditional
        Probability Distribution (CPD) tables from the json config if they are
        present, that passes all the information to `ComponentBN` to create
        the BN object.
        """
        with open(self.bn_config_file, 'r') as fin:
            data = json.load(fin)
        CPD_list = []
        CPD_cfg = data.pop("CPDs", None)
        if CPD_cfg is not None:
            for name, config in CPD_cfg.items():
                CPD_list.append(TabularCPD(**config))
        else:
            CPD_list = None
        self.BN = ComponentBN(**data, CPDs=CPD_list)

    def forward(self, size=1):
        """
        Randomly samples from the BN to determine the outcome.

        Args:
            size (int): number of time to sample from the BN

        Returns:
            np.array of length `size` with values of 1 where condition of
            success is met and 0 otherwise. If `size` is 1, then returns single
            integer value.
        """
        res = self.BN.get_sample(
            evidence=self.arguments,
            size=size
        )[self.outcome]
        if size == 1:
            return np.where(res == self.condition, 1, 0)[0]
        else:
            return np.where(res == self.condition, 1, 0)

