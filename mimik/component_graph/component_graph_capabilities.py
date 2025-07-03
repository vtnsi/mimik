import networkx as nx
from mimik.component_graph.component_graph import ComponentGraph
from scipy.stats import bernoulli


class ComponentGraphCapabilities:
    def __init__(self, graph: ComponentGraph):
        """
        A constructor for the ComponentSimulation class

        Parameters:
            graph (ComponentGraph): A networkx graph containing the nodal information
        """
        self.graph = graph
        self.root_components = self.graph.get_start_components()
        self.valid_paths = self.get_all_paths()
        self.__monte_carlo_outcomes = {}
        self.__monte_carlo_probabilities = {}

    def validate_graph(self, graph: ComponentGraph) -> bool:
        """
        Validates the ComponentGraph to ensure each component has a task

        Args:
            graph (ComponentGraph): The graph to validate

        Returns:
            bool: True if the ComponentGraph has a task for each component
        """
        for node_name in graph.nodes.keys():
            if graph.nodes[node_name]["component"].task == None:
                return False
        return True

    def get_monte_carlo_outcomes(self):
        """
        Returns the outcome of the Monte Carlo simulation

        Returns:
            dict: A dictionary mapping paths to arrays containing results
        """
        return self.__monte_carlo_outcomes
    
    def get_monte_carlo_probabilities(self):
        """
        Returns the probabilities derived from the Monte Carlo simulation

        Returns:
            dict: A dictionary mapping paths to arrays containing path probabilities
        """
        return self.__monte_carlo_probabilities

    def get_all_paths(self):
        """
        Gets a list of all paths in the killweb that are capable of accomplishing
        each task

        Returns:
            list[str]: A list of paths resembling kill chains
        """
        paths = []
        for start_component in self.graph.get_start_components():
            for end_component in self.graph.get_end_components():
                simple_paths = nx.all_simple_paths(
                    self.graph,
                    source=start_component,
                    target=end_component,
                )
                for path in simple_paths:
                    paths.append(path)
        return paths

    def print_all_paths(self):
        """
        Prints all of the paths in the component graph
        """
        for path in self.valid_paths:
            print(self.__format_path_string(path))
        print("\nThere are %d paths through the killweb" % len(self.valid_paths))

    def monte_carlo_simulation(self, num_iterations: int):
        """
        Gets a list of success probabilities for each path and sorts them

        Parameters:
            num_iterations (int): The number of times to calculate probability of a path
                for an average
            
        Returns:
            The probability list of each simple path over num_iterations
        """
        if self.validate_graph(self.graph):
            self.__monte_carlo_outcomes = {}
            self.__monte_carlo_probabilities = {}
            for path in self.get_all_paths():
                path_string = self.__format_path_string(path)
                self.__monte_carlo_outcomes[path_string] = []
                self.__monte_carlo_probabilities[path_string] = []
                for _run_number in range(0, num_iterations):
                    single_outcome = [0] * len(path)
                    single_probability = [0] * len(path)
                    for index, component_name in enumerate(path):
                        component = self.graph.nodes[component_name]["component"]
                        single_probability[index] = component.task.forward()
                        if bernoulli.rvs(single_probability[index]) != 1:
                            break
                        single_outcome[index] = 1
                    self.__monte_carlo_outcomes[path_string].append(single_outcome)
                    self.__monte_carlo_probabilities[path_string].append(single_probability)
        elif not self.graph.silent:
            print("ComponentGraph was not valid for creation of ComponentMetrics. Please ensure each component has an associated task complete with a task name and arguments")

    def __format_path_string(self, path) -> str:
        """
        Formats the path string by removing unwanted characters
        
        Parameters:
            path (Any): The path string to format
        
        Returns:
            The formatted path string
        """
        str_path = str(path)
        for replace_chars in ['[', ", 'center'", ']', "'"]:
            str_path = str_path.replace(replace_chars, "")
        return str_path