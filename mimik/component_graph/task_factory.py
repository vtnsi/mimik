import os
import importlib
import sys
import inspect
from mimik.component_graph.abstract_task import AbstractTask


class TaskFactory():
    def __init__(self, task_folder: str, silent: bool):
        """
        Creates a TaskFactory object which loads all modules from the given task_folder
        Utilizes a variation of the Factory design pattern.

        Parameters:
            task_folder (str): The folder to load task modules from
            silent (bool): True if MIMIK is running in silent mode

        Raises:
            FileNotFoundError: If the task_folder cannot be found
        """
        self.localizers = {}
        try:
            for module in os.listdir(task_folder):
                if module[-3:] == ".py":
                    with open(os.path.join(task_folder, module)) as task_file:
                        lines = task_file.readlines()
                        for line in lines:
                            if "class" in line and "AbstractTask" in line:
                                class_name = line.split('(')[0].replace("class ", "")
                                module_name = module[:-2] + class_name
                                spec = importlib.util.spec_from_file_location(module_name, os.path.join(task_folder, module))
                                loaded_module = importlib.util.module_from_spec(spec)
                                spec.loader.exec_module(loaded_module)
                                sys.modules[module_name] = loaded_module
                                for name, obj in inspect.getmembers(loaded_module):
                                    if inspect.isclass(obj) and name == class_name:
                                        self.localizers[class_name] = obj
        except FileNotFoundError:
            if not silent:
                print("No tasks directory was found. Continuing with assumption that all tasks use static probability.")

    def create_task(self, task_name: str, arguments: dict):
        """
        Attempts to return a task associated with the given name. If the
        task cannot be found, an AbstractTask is returned instead that assumes
        a static probability is found within the arguments parameter.

        Parameters:
            task_name (str): The name of the task to create
            arguments (dict): The dictionary of arguments to include for the given
                task

        Returns:
            The created task
        """
        try:
            #print(task_name, arguments)
            return_task = self.localizers[task_name](arguments)
        except KeyError as e:
            if "probability" in arguments.keys() or task_name == 'Other':
                return_task = AbstractTask(task_name, arguments)
            else:
                raise KeyError("The provided task name could not be associated with a module found in the provided task directory.")
        return return_task
