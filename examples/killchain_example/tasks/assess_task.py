# -*- coding: utf-8 -*-
"""
Created on Mon May 12 11:27:06 2025

Task classes for MIMIK tutorial

"""


from mimik.component_graph.abstract_task import AbstractTask


class AssessTask(AbstractTask):
    
    def __init__(self, arguments: dict):
        '''
        Initialize custom Assess task

        Parameters
        ----------
        arguments : dict
            dictionary of arguments
        '''
        
        super().__init__("AssessTask", arguments)
        self.p = arguments['p']
        
    def forward(self):
        return self.p