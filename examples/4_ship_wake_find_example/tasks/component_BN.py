from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.estimators import MaximumLikelihoodEstimator, BayesianEstimator
from pgmpy.sampling import BayesianModelSampling
from pgmpy.factors.discrete import State
from pandas import DataFrame
import networkx as nx
import pandas as pd


class ComponentBN(object):
    def __init__(
        self,
        edges: list,
        CPDs: dict=None,
        data: DataFrame=None,
        estimator: str="MaximumLikelihood",
        **kwargs
    ):
        """
        Constructor for class to create a Bayesian Network (BN) to model
        component system in Killweb

        This class creates a BN using pgmpy and wraps several of the methods
        for inferring and sampling from the BN, and it creates a flexible
        interface for creating the BN

        Parameters:
            edges (list[tuple]): list of tuples for the nodes and edges of the
                graph that defines the BN.
            CPDs (dict[str:TabularCPD] or list[TabularCPD]): Conditional
                Probability Distribution (CPD) tables that define the
                relationship of the edges. Intended for manual creation of
                tables and should be None of using data.
            data (DataFrame): pandas dataframe containing data for estimating
                conditional probabilities. If using data, CPDs should be None.
            estimator (str): name of the estimator to use with data to get the
                conditional probabilies. Should either be "MaximumLikelihood"
                or "BayesianEstimator". If using "BayesianEstimator" additional
                kwargs can be specified for setting up a prior distribution
                then updating based on data provided.
        """
        self.edges = edges
        self.model = BayesianNetwork(ebunch=self.edges)
        self.CPDs = CPDs
        self.data = data
        self.estimator = estimator
        self.kwargs = kwargs
        self.__create_infer_models()

    def __create_infer_models(self):
        """
        Creates the BN model from either the CPDs or the data kwargs provided,
        then creates the inferences and sampling objects of the BN model.
        """
        if self.CPDs is not None:
            if type(self.CPDs) is dict:
                for name, cpd in self.CPDs.items():
                    self.model.add_cpds(cpd)
            else:
                for cpd in self.CPDs:
                    self.model.add_cpds(cpd)

        elif self.data is not None:
            if type(self.data) is str:
                self.data = pd.read_csv(self.data)

            if self.estimator == "MaximumLikelihood":
                self.model.fit(self.data, estimator=MaximumLikelihoodEstimator)
            elif self.estimator == "Bayesian":
                self.model.fit(self.data, estimator=BayesianEstimator,
                               **self.kwargs)

        else:
            raise ValueError("Need to specify CPDs or data for componentBN")

        self.infer_model = VariableElimination(self.model)
        self.sampling_model = BayesianModelSampling(self.model)

    def get_infer(
        self,
        evidence: dict,
        variables: list,
        joint: bool=True,
        virtual_evidence: list=None,
    ):
        """
        Infer from the BN model for a particular query defined by:

        Parameters:
            evidence (dict[str:str]): dictionary that defines the name of a
                nodes in the graph and the outcome observed at each node as a
                key value pair ({node: outcome}
            variables (list): list of the nodes to return the probability
                tables for after updating based on the evidence provided. Can
                be a list with a single item.
            joint (bool): if multiple nodes listed in variables, then joint is
                True will return single table with combination of all the
                outcomes of all the variables, if joint is False then a
                separate table will be returned for each node in variables
            virtual_evidence (list[TabularCPD]): instead of providing
                definitive outcomes for evidence, virtual evidence provides
                probabilities for each possible outcome of a node. For example,
                if node "A" has two possible outcomes and we think that the
                outcome is 40% probability outcome "X" and 60% for "Y" we can
                specify this evidence as:
                    TabularCPD(variable="A", variable_card=2, values=[[0.4],
                    [0.6]], state_names={"A": ["X", "Y"])
                This can also be useful if specifying evidence could alter
                nodes the user does not wish to change, for example if the
                evidence provided might effect node "A" but we want it to have
                the same probability table it was initialized with then we can
                specify that again here. This is a more advanced function and
                for most use cases this should be left None.

        Returns:
            A pgmpy DiscreteFactor object that contains the probability table
            for node(s) in variables list. The user can print this object to
            see a formated version of the table.

        """
        return self.infer_model.query(
            variables=variables,
            evidence=evidence,
            virtual_evidence=virtual_evidence,
            joint=joint,
        )

    def get_sample(
        self,
        evidence: dict,
        size: int=1,
    ):
        """
        Samples from the BN based on the evidence provided. Evidence nodes are
        set, the other nodes are updated based on these values, then the BN
        is randomly sampled from all nodes.

        Parameters:
            evidence (dict[str:str]): dictionary that defines the name of a
                nodes in the graph and the outcome observed at each node as a
                key value pair ({node: outcome}
            size (int): the number of times to sample from the BN.

        Returns:
            A dataframe of shape (n, m) where n=size and m is the number of
            nodes in the graph. Each row is a random sample from the BN after
            updating for evidence.

        """
        evidence_list = []
        for k, v in evidence.items():
            evidence_list.append(State(k, v))
        return self.sampling_model.likelihood_weighted_sample(
            evidence=evidence_list,
            size=size
        )

    def get_prob_success(
        self,
        evidence: dict,
        virtual_evidence=None,
        **kwargs
    ):
        """
        Runs inference on the BN, similar to the `get_infer` method, but
        instead of returning a table of probabilities returns a single
        probability for the node and outcome specified by the user.

        Parameters:
            evidence (dict[str:str]): dictionary that defines the name of a
                nodes in the graph and the outcome observed at each node as a
                key value pair ({node: outcome}
            virtual_evidence (list[TabularCPD]): instead of providing
                definitive outcomes for evidence, virtual evidence provides
                probabilities for each possible outcome of a node. For example,
                if node "A" has two possible outcomes and we think that the
                outcome is 40% probability outcome "X" and 60% for "Y" we can
                specify this evidence as:
                    TabularCPD(variable="A", variable_card=2, values=[[0.4],
                    [0.6]], state_names={"A": ["X", "Y"])
                This can also be useful if specifying evidence could alter
                nodes the user does not wish to change, for example if the
                evidence provided might effect node "A" but we want it to have
                the same probability table it was initialized with then we can
                specify that again here. This is a more advanced function and
                for most use cases this should be left None.
            kwargs (dict): user must provide a key-value pair for the node and
                outcome of interest (i.e., the successful outcome). For
                example, if we want to know the probability that node "A" has
                outcome "X" the user should provide A="X" as an argument to
                this method. NOTE: the name of the node is treated as a
                variable name, it should NOT have any quotation marks.

        Returns:
            float for the probability that the specified node will have the
            outcome of interest.

        """
        return self.infer_model.query(
            variables=list(kwargs.keys()),
            virtual_evidence=virtual_evidence,
            evidence=evidence
        ).get_value(**kwargs)

    def draw_network(self):
        """
        Creates a figure for the graph of the bayesian network.
        """
        nx_graph = nx.DiGraph(self.model.edges())
        nx.draw_shell(nx_graph, with_labels=True, font_weight='bold')
