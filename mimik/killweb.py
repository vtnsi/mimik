import os
from mimik.component_graph.component_graph import ComponentGraph
from mimik.component_graph.component_graph_metrics import ComponentGraphCapabilities
from mimik.component_graph.component_graph_metrics import ComponentGraphMetrics
from mimik.json_validator import JsonValidator


class Killweb:
    def __init__(
        self, 
        working_dir: str=os.getcwd(),
        config_file: str=None, 
        silent: bool=False, 
        view=None
    ):
        """
        A constructor for the Killweb class

        In this MVC design pattern, this class is the Controller. The majority of methods
        within this class are wrappers for functionality that exists within the Model (i.e.)

        Parameters:
            config_file (str): The JSON file containing all of the killweb config information.
            working_dir (str): The directory marked to contain the configs, tasks, and output sub directories.
                Default is current working directory.
            silent (bool): True if MIMIK is running in silent mode. Default is False.
            view (Renderer): The Renderer object associated with running MIMIK with a GUI.
                Default is None.
        """
        self.working_dir = working_dir
        if not os.path.isdir(self.working_dir):
            os.mkdir(self.working_dir)
        self.component_graph = ComponentGraph(working_dir=self.working_dir, silent=silent)
        if config_file != None:
            validator = JsonValidator()
            validator.validate_config(config_file, silent)
            self.load_killweb_from_config_file(config_file)
        else:
            self.__update_killweb(False)

    def __update_killweb(self, display_graphs: bool):
        """
        Updates the ComponentCapabilities and ComponentMetrics after the
        component graph is updated

        Args:
            display_graphs (bool): True if the graphs should be displayed
        """
        self.component_capabilities = ComponentGraphCapabilities(self.component_graph)
        self.component_metrics = ComponentGraphMetrics(self.component_capabilities)

    def save_killweb_to_config_file(self, filename: str, killweb_name="killweb"):
        """
        Saves the current killweb's component graph to a config file

        Args:
            filename (str): The file to save to
            killweb_name (str): The name of the killweb
        """
        self.component_graph.save_killweb_to_config_file(filename, killweb_name)

    def load_killweb_from_config_file(self, filename: str):
        """
        Loads a killweb from a given config file
        
        Args:
            filename (str): The file to load from
        """
        self.component_graph.load_killweb_from_config_file(filename)
        self.__update_killweb(True)

    def create_component_networkx_visualization(self, show_and_save=True):
        """
        Creates and displays a networkx visualization for the component graph
        and saves the output to the ouput directory

        Args:
            show_and_save (bool): True if the graph should be shown in save.
                Typically true when running without the GUI
        """
        return self.component_graph.networkx_visualization(show_and_save)

    def add_new_component(
        self, 
        component_name: str, 
        to_components: list[str]=None, 
        from_components: list[str]=None, 
        component_attributes: dict=None
    ):
        """
        Adds a new component to the existing component graph

        Args:
            component_name (str): The name of the new component
            task_name (str): The task the new component can complete
            task_arguments (dict): A dictionary of arguments required for the task's forward function
            from_components (list[str]): A list of names of components the new component can receive from
            to_components (list[str]): A list of names of components the new component can output to
        """
        self.component_graph.add_new_component(component_name, to_components, from_components, component_attributes)
        self.__update_killweb(True)

    def add_task_to_component(self, component_name: str, task_name: str, task_arguments: dict):
        """
        Create a new task and add it to a new component

        Args:
            component_name (str): The name of the component to update
            task_name (str): The name of the task to create
            task_arguments (dict): The arguments to create the task with
        """
        self.component_graph.add_task_to_component(component_name, task_name, task_arguments)
        self.__update_killweb(True)

    def add_new_edge(self, from_component_name: str, to_component_name: str):
        """
        Adds a new edge between 2 components
        
        Parameters:
            from_component_name (str): The component pointing to "to_component"
            to_component_name (str): The component being pointed to by "from_component"
        """
        self.component_graph.add_new_edge(from_component_name, to_component_name)
        self.__update_killweb(True)

    def remove_component(self, component_name: str):
        """
        Removes

        Args:
            component_name (str): _description_
        """
        self.component_graph.remove_component(component_name)
        
    def remove_edge(self, from_component_name: str, to_component_name: str):
        """
        Removes a new edge between 2 components
        
        Parameters:
            from_component_name (str): The component pointing to "to_component"
            to_component_name (str): The component being pointed to by "from_component"
        """
        self.component_graph.remove_existing_edge(from_component_name, to_component_name)
        self.__update_killweb(True)
        
    def print_nodes(self):
        """
        Print all nodes in the killweb
        """
        print(self.component_graph.nodes)
        
    def print_edges(self):
        """
        Print all edges in the killweb
        """
        print(self.component_graph.edges)
        

    def get_all_paths_in_killweb(self):
        """
        Gets all of the paths in the killweb that include each task

        Returns:
            list[str]: A list of all paths in the killweb such that each
                task can be completed
        """
        return self.component_capabilities.get_all_paths()

    def print_all_paths_in_killweb(self):
        """
        Print all of the paths in the killweb across the component graph
        """
        self.component_capabilities.print_all_paths()

    def monte_carlo_on_paths(self, num_iterations: int):
        """
        Runs a Monte Carlo simulation num_iterations times across all paths within the killweb

        Args:
            num_iterations (int): The number of monte carlo iterations to execute
        """
        self.component_capabilities.monte_carlo_simulation(num_iterations)

    def get_monte_carlo_results(self):
        """
        Returns a tuple consisting of the monte carlo algorithm results and probability
        distributions

        Returns:
            A tuple containing the current monte carlo outcomes and probabilities
        """
        return self.component_capabilities.get_monte_carlo_outcomes(), self.component_capabilities.get_monte_carlo_probabilities()

    def get_probabilities_of_paths(self):
        '''
        Returns the probability of success for each path after Monte Carlo sim

        Returns
        -------
        dictionary of success probabilities
        '''
        probability_of_success, _ = self.component_metrics.calc_stats_of_paths()
        return probability_of_success
    
    def get_avg_number_success_events(self):
        '''
        Returns the average number of successful events for each path

        Returns
        -------
        dictionary of average number of successful events
        '''
        _, avg_num_success_events = self.component_metrics.calc_stats_of_paths()
        return avg_num_success_events

    def print_probabilities_of_paths(self, amount_to_print=None, selected_component=None):
        """
        Prints the amount_to_print number of paths with the highest probability
        of success. By default, all paths will be printed if no number is specified

        Args:
            amount_to_print (int): The amount of paths to print. By defaults this is none
                which will print all paths
            selected_component (str): The name of the components to be included in all displayed paths
        """
        self.component_metrics.print_probability_of_paths(amount_to_print, selected_component)
    
    def print_proportion_complete(self, path_to_test: str):
        """
        Prints the proportion of complete (successful) path_to_tests compared to the
        incomplete (failed) path_to_test based on the results of the Monte Carlo simulation

        Args:
            path_to_test (str): The specific path to view the proportion of complete paths
        """
        prop_complete = self.component_metrics.proportion_complete(path_to_test)
        print("Proportion of complete kill chains: %s" % str(prop_complete))
        return prop_complete

    def print_average_number_of_successes(self, path_to_test: str):
        """
        Prints the average number of successful events across the path_to_test
        based on the results of the Monte Carlo simulation

        Args:
            path_to_test (str): The specific path to view the average number of successes
        """
        avg_success = self.component_metrics.average_num_success(path_to_test)
        print("Average number of success events: %s" % str(avg_success))
        return avg_success

    def print_variance(self, path: list[str]) -> float:
        """
        Prints the variance of the outcomes from the Monte Carlo simulation

        Parameters:
            path (list[str]): The path to calculate variance from
        
        Returns:
            float: The variance
        """
        variance = self.component_metrics.calculate_variance(path)
        print("The variance from the monte carlo results is: %s" % str(variance))
        return variance

    def plot_monte_carlo_distribution(self, path_to_test: str):
        """
        Plots the monte carlo results of each component within the path_to_test 
        based on the results of the Monte Carlo simulation

        Args:
            path_to_test (str): The path whose Monte Carlo results are to be plot
        """
        self.component_metrics.plot_MC_distribution(path_to_test)

    def calculate_node_centrality(self):
        """
        Calculates the centrality of each node.

        As the component graph is also a directional graph, there is an in and out
        centrality for each node. Both will be displayed assuming the centrality has
        a value > 0

        Returns:
            list[tuple]: A list of tuples of (centrality, component_name)
        """
        return self.component_metrics.compute_node_centrality()
