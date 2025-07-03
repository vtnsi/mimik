import matplotlib.pyplot as plt
import numpy as np
import copy
import os
import math
import networkx as nx
from mimik.component_graph.component_graph_capabilities import ComponentGraphCapabilities


class ComponentGraphMetrics:
    def __init__(self, capabilities: ComponentGraphCapabilities):
        """
        A constructor for the ComponentSimulation class

        Parameters:
            capabilities (ComponentGraphCapabilities): The capabilities object associated with a ComponentGraph
        """
        self.capabilities = capabilities
        
    def calc_stats_of_paths(self):
        """
        Calculates the probability of success for each path after Monte Carlo sim

        Returns:
            A dictionary of probabilities
        """
        if len(self.capabilities.get_monte_carlo_outcomes()) == 0:
            print("Please run the monte_carlo_simulation function before as this function utilizes those results.")
            return
        
        probability_of_success = {}
        average_success_events = {}
        for path in self.capabilities.get_monte_carlo_outcomes().keys():
            probability_of_success[path] = self.proportion_complete(path.split(", "))
            average_success_events[path] = self.average_num_success(path.split(", "))
        probability_of_success = {k: v for k, v in sorted(probability_of_success.items(), key=lambda item: item[1])}
        return probability_of_success, average_success_events
        

    def print_probability_of_paths(self, print_top_n_paths=None, selected_component=None):
        """
        Gets a list of success probabilities for each path and sorts them

        Parameters:
            print_top_n_paths (int): Print the X number of paths with the highest probability
            selected_component (str): The path whose node should be included in the path

        Returns:
            The probability list of each simple path
        """
        if len(self.capabilities.get_monte_carlo_outcomes()) == 0:
            print("Please run the monte_carlo_simulation function before as this function utilizes those results.")
            return
        probability_of_success, average_success_events = self.calc_stats_of_paths()
        count = 0
        for path in reversed(probability_of_success.keys()):
            if (print_top_n_paths is None or count < print_top_n_paths) and (selected_component is None or selected_component in path):
                print("Path: %s\n\tProbability of Success: %s\n\tAverage Number of Successful Events: %s" % (path, str(probability_of_success[path]), str(average_success_events[path])))
            count += 1

    def proportion_complete(self, path: list[str]) -> float:
        """
        Calculates the proportion of simulations that succeed through the path

        Parameters:
            path (list[str]): The path to check the proportion of iterations that succeed

        Returns:
            The proportion of times the path succeed to when it doesn't
        """
        if len(self.capabilities.get_monte_carlo_outcomes()) == 0:
            print("Please run the monte_carlo_simulation function before as this function utilizes those results.")
            return
        monte_carlo_array = np.array(self.capabilities.get_monte_carlo_outcomes()[self.convert_path_to_string(path)])
        return np.sum(monte_carlo_array[:, -1]) / monte_carlo_array.shape[0]

    def average_num_success(self, path: list[str]) -> float:
        """
        Calculates the average number of success events for each component in a path

        Parameters:
            path (list[str]): The path to check the average number of successful components

        Returns:
            The average number of successful components within the path
        """
        if len(self.capabilities.get_monte_carlo_outcomes()) == 0:
            print("Please run the monte_carlo_simulation function before as this function utilizes those results.")
            return
        monte_carlo_array = np.array(self.capabilities.get_monte_carlo_outcomes()[self.convert_path_to_string(path)])
        return np.sum(monte_carlo_array) / monte_carlo_array.shape[0]

    def calculate_variance(self, path: list[str]) -> float:
        """
        Calculates the variance of the monte carlo outcomes

        Parameters:
            path (list[str]): The path to calculate variance from

        Returns:
            float: The variance of the monte carlo outcomes
        """
        if len(self.capabilities.get_monte_carlo_outcomes()) == 0:
            print("Please run the monte_carlo_simulation function before as this function utilizes those results.")
            return
        string_path = self.capabilities.get_monte_carlo_outcomes()[self.convert_path_to_string(path)]
        return np.var([path_result[-1] for path_result in list(string_path)])

    def plot_MC_distribution(self, path: list[str]):
        """
        Plot the distrubtion of successes across the components within a path

        Parameters:
            path (list[str]): The path whose components are to be plotted with respect
                to their distribution of successful events
        """
        if len(self.capabilities.get_monte_carlo_outcomes()) == 0:
            print("Please run the monte_carlo_simulation function before as this function utilizes those results.")
            return
        monte_carlo_array = np.array(self.capabilities.get_monte_carlo_outcomes()[self.convert_path_to_string(path)])
        proportion = np.sum(monte_carlo_array, axis=0) / monte_carlo_array.shape[0]
        events = []
        for component_name in path:
            events.append(component_name)
        fig, ax = plt.subplots()
        fig.set_figwidth(6)
        fig.set_figheight(6)
        ax.bar(events, proportion)
        ax.set_ylabel("Proportion")
        ax.set_xlabel("Events in Kill Chain")
        ax.set_ylim([0, 1])
        ax.set_title("Distribution of Successful Events")
        plt.savefig(os.path.join(self.capabilities.graph.output_dir, "mc_distribution.png"))
        plt.show()

    def compute_node_centrality(self):
        """
        Computes and sorts the in and out centrality of each component of the graph

        Returns:
            A list of two arrays each containing a list of key value pairs of components to their centralities
        """
        in_degree_centrality = nx.in_degree_centrality(self.capabilities.graph)
        out_degree_centrality = nx.out_degree_centrality(self.capabilities.graph)
        return_array = []
        for index, centrality in enumerate([in_degree_centrality, out_degree_centrality]):
            for component in list(centrality.keys()):
                centrality[component] *= len(self.capabilities.graph.nodes) - 1
                if centrality[component] == 0:
                    del centrality[component]
            return_array.append(
                sorted(
                    ((v,k) for k,v in centrality.items() if v != 0.0),
                    reverse=True
                )
            )
        current_centrality = "in"
        for degree_setting in return_array:
            if current_centrality == "in":
                print("In Degree Centrality")
            else:
                print("\nOut Degree Centrality")
            for pair in degree_setting:
                print("\t%s has an %s centrality of %d" % (pair[1], current_centrality, int(pair[0])))
            current_centrality = "out"
        return return_array

    def convert_path_to_string(self, path: list[str]) -> str:
        """
        Converts a path, definied as a list of node names, to a single string

        Args:
            path (list[str]): The path to convert

        Returns:
            A string representation of the path
        """
        return ", ".join(path)
