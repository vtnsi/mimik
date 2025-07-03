import json
import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from mimik.component_graph.component import Component
from mimik.component_graph.task_factory import TaskFactory


class ComponentGraph(nx.DiGraph):
    def __init__(self, working_dir: str, silent=False):
        """
        Creates a new ComponentGraph object

        Args:
            working_dir (str): The working directory to read from
            silent (bool): True if MIMIK is running in silent mode
        """
        super().__init__()
        plt.close()
        self.silent = silent
        self.output_dir = os.path.join(working_dir, "output")
        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)
        self.task_factory = TaskFactory(os.path.join(working_dir, "tasks"), silent)
        self.mission_tasks = []

    def get_start_components(self):
        """
        Gets all of the components starting a path in the killweb

        Returns:
            list[str]: A list of component names for nodes who start paths
        """
        return [component for component in self.nodes if self.in_degree(component) == 0]

    def get_end_components(self):
        """
        Gets all of the components ending a path in the killweb

        Returns:
            list[str]: A list of component names for nodes who end paths
        """
        return [component for component in self.nodes if self.out_degree(component) == 0]

    def save_killweb_to_config_file(self, filename: str, killweb_name: str):
        """
        Saves the current killweb to a file

        Args:
            filename (str): The file path to save to
            killweb_name (str): The name of the killweb to save 
        """
        killweb_dict = {killweb_name: {}}
        for component in self.nodes.keys():
            killweb_dict[killweb_name][component] = {}
            killweb_dict[killweb_name][component]["attributes"] = {}
            current_component = self.nodes[component]["component"]
            attributes_dict = killweb_dict[killweb_name][component]["attributes"]
            if current_component.task != None:
                attributes_dict["task"] = current_component.task.task_name
                attributes_dict["task_arguments"] = current_component.task.task_arguments
            if current_component.system_name != None:
                attributes_dict["system_name"] = current_component.system_name
            killweb_dict[killweb_name][component]["connected_components"] = current_component.connected_component_names
        with open(filename, 'w') as file:
            json.dump(killweb_dict, file, indent=4)

    def load_killweb_from_config_file(self, config_filename: str):
        """
        Loads a killweb from a given config file

        Args:
            killweb_name (str): The name of the killweb to load
            config_filename (str): The config file to load from
        """
        with open(config_filename, 'r') as file:
            data = json.load(file)
            for killweb in data.values():
                for component in killweb.keys():
                    if "attributes" in killweb[component]:
                        self.add_new_component(component, killweb[component]["connected_components"], [], killweb[component]["attributes"])
                    else:
                        self.add_new_component(component, killweb[component]["connected_components"], [], {})
                break

    def add_new_component(self, component_name: str, to_components: list[str], from_components: list[str], component_attributes: dict):
        """
        Adds a new component to the killweb

        Args:
            component_name (str): The name of the component to add
            to_components (list[str]): A list of the components the new component points to
            from_components (list[str]): A list of components the new component is pointed to by
            component_attributes (dict): A dictionary of component attributes including task,
                task_arguments, and system_name
        """
        component_name = component_name.strip()
        stripped_to_components = []
        
        # add out edges
        if isinstance(to_components, list):
            for to_component in to_components:
                stripped_to_components.append(to_component.strip())
        component = Component(component_name, stripped_to_components)
            
        if component_name in self.nodes():
            nx.set_node_attributes(self, {component_name: {"component": component}})
        else:
            self.add_node(component_name, component=component)
            
        if isinstance(from_components, list):
            for from_component in from_components:
                from_component = from_component.strip()
                if from_component not in self.nodes():
                    new_from_component = Component(from_component, [component_name])
                    self.add_node(from_component, component=new_from_component)
                self.add_edge(from_component, component_name)
                self.nodes[from_component]["component"].connected_component_names.append(component_name)
          
        if isinstance(to_components, list):
            for to_component in stripped_to_components:
                if to_component not in self.nodes():
                    new_to_component = Component(to_component, [])
                    self.add_node(to_component, component=new_to_component)
                self.add_edge(component_name, to_component)
            
        if isinstance(component_attributes, dict):
            for attribute in component_attributes.keys():
                if "task_arguments" == attribute:
                    continue
                elif "task" == attribute and "task_arguments" in component_attributes:
                    self.add_task_to_component(component_name, component_attributes["task"], component_attributes["task_arguments"])
                elif "system_name" == attribute:
                    self.nodes[component_name]["component"].add_system_name(component_attributes["system_name"])
                else:
                    self.nodes[component_name][attribute] = component_attributes[attribute]

    def add_task_to_component(self, component_name: str, task_name: str, task_arguments: dict):
        """
        Adds a task to an existing component

        Args:
            component_name (str): The name of the component to update
            task_name (str): The name of the task to add
            task_arguments (dict): The arguments of the task to add
        """
        if task_name not in self.mission_tasks:
            self.mission_tasks.append(task_name)
        new_task = self.task_factory.create_task(task_name, task_arguments)
        self.nodes[component_name]["component"].add_task(new_task)

    def add_new_edge(self, from_component: str, to_component: str):
        """
        Adds a new edge to the killweb

        Args:
            from_component (str): The origin component of the new edge
            to_component (str): The destination component of the new edge
        """
        if self.nodes[from_component] != None and self.nodes[to_component] != None:
            self.add_edge(from_component, to_component)
            self.nodes[from_component]["component"].connected_component_names.append(to_component)

    def remove_component(self, component_name: str):
        """
        Removes a component of the given name

        Args:
            component_name (str): The name of the component to be removed
        """
        for from_component in list(self.predecessors(component_name)):
            self.nodes[from_component]["component"].connected_component_names.remove(component_name)
        self.remove_node(component_name)
        
    def remove_existing_edge(self, from_component: str, to_component: str):
        """
        Removes an edge from the killweb

        Args:
            from_component (str): The origin component of the removed edge
            to_component (str): The destination component of the removed edge
        """
        if self.has_edge(from_component, to_component):
            self.remove_edge(from_component, to_component)
            self.nodes[from_component]["component"].connected_component_names.remove(to_component)

    def update_annotation(self, index):
        """
        Updates the annotation box with the hovered node contents

        Parameters:
            index (int): The index of the node being hovered over
        """
        node_index = index["ind"][0]
        component = list(nx.get_node_attributes(self, "component").values())[node_index]
        component_name = component.full_name
        xy = self.pos[component_name]
        self.annot.xy = xy
        node_attr = {"Component Name": component_name}
        if component.task != None:
            node_attr["Task"] = component.task.task_name
        if component.system_name != None:
            node_attr["System"] = component.system_name

        node_attr.update(self.nodes[component_name])
        text = "\n".join(f"{k}: {v}" for k, v in node_attr.items() if k != "component")
        self.annot.set_horizontalalignment('left')
        if self.annot.get_window_extent().x1 > self.fig.get_window_extent().x1:
            self.annot.set_horizontalalignment('right')
        self.annot.set_text(text)

    def hover(self, event):
        """
        The function to be called whenever the mouse hovers over the canvas.
        Checks if a node is being hovered over, and update the annotation box
        if so.

        Parameters:
            event: The hover event action including position data
        """
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            cont, index = self.graph_nodes.contains(event)
            if cont:
                self.update_annotation(index)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.fig.canvas.draw_idle()

    def get_component_on_click(self, event):
        """
        Given a click event, determine what, if any, component was clicked

        Args:
            event (Event): A mouse click event

        Returns:
            Component: A component whose node in the graph was clicked on,
                or None if no component was clicked
        """
        if event.inaxes == self.ax:
            cont, index = self.graph_nodes.contains(event)
            if cont:
                return list(nx.get_node_attributes(self, "component").values())[index["ind"][0]]
        return None

    def networkx_visualization(self, show_and_save=True):
        """
        Creates a star graph visualization by utilizing networkx to plot
        our existing nodes, edges, and attributes

        Args:
            show_and_save (bool): True if the graph should be shown in save.
                Typically true when running without the GUI

        Returns:
            The created PyPlot figure
        """
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.fig.subplots_adjust(right=3, top=3)
        self.pos = nx.spring_layout(
            self.to_undirected(), seed=0, k=0.2
        )
        self.pos[""] = np.array([0, 0])
        for node in self.nodes.keys():
            if "x" in self.nodes[node] and "y" in self.nodes[node]:
                self.pos[node] = np.array([self.nodes[node]["x"], self.nodes[node]["y"]])
        self.graph_nodes = nx.draw_networkx_nodes(
            self, pos=self.pos, ax=self.ax, node_size=70
        )
        nx.draw_networkx_edges(self, pos=self.pos, ax=self.ax)
        plt.axis("off")
        self.annot = self.ax.annotate(
            "",
            xy=(0, 0),
            xytext=(20, 20),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->"),
            horizontalalignment='left', verticalalignment='bottom'
        )
        self.annot.set_visible(False)
        self.fig.tight_layout()
        self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
        if show_and_save:
            plt.show()
            pygraphviz_model = nx.nx_agraph.to_agraph(self)
            pygraphviz_model.graph_attr.update(overlap="scale")
            pygraphviz_model.draw(
                os.path.join(self.output_dir, "component_networkx_model.png"), prog="neato"
            )
        return self.fig
