from mimik.component_graph.abstract_task import AbstractTask


class Component:
    def __init__(
        self,
        name: str,
        connected_component_names: list[str]
    ):
        """
        A constructor for the Component class

        Parameters:
            name (str): The component's name
            connected_component_names (list[str]): A list of all components connected to
                this component
        """
        self.full_name = name
        self.connected_component_names = connected_component_names
        self.task = None
        self.system_name = None

    def add_task(self, task: AbstractTask):
        """
        Adds a task to the Component

        Args:
            task (AbstractTask): The task to add to the component
        """
        self.task = task

    def add_system_name(self, system_name: str):
        """
        Adds a system name to the component

        Args:
            system_name (str): The system name to be added to the component
        """
        self.system_name = system_name
