# -*- coding: utf-8 -*-
"""
Created on Mon May 12 11:27:06 2025

Task classes for MIMIK tutorial

"""

from mimik.component_graph.abstract_task import AbstractTask


class Fix(AbstractTask):
    '''
    Class for the Fix task
    '''
    
    def __init__(self, arguments: dict):
        '''
        Initialize custom Fix task

        Parameters
        ----------
        arguments : dict
            dictionary of arguments
        '''
        
        super().__init__("Fix", arguments)
        self.success_probability = arguments['success_probability']
        
    def forward(self):
        return self.success_probability