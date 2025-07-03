# -*- coding: utf-8 -*-
"""
Created on Mon May 12 11:27:06 2025

Task classes for MIMIK tutorial

"""

from scipy.stats import beta, gamma

from mimik.component_graph.abstract_task import AbstractTask


class TrackTask(AbstractTask):
    '''
    Class for the beta Bernoulli prior
    '''
    
    def __init__(self, arguments: dict):
        '''
        Initialize custom Fix task

        Parameters
        ----------
        arguments : dict
            dictionary of arguments
        '''
        
        super().__init__("TrackTask", arguments)
        self.k = arguments['k']
        self.theta = arguments['theta']
        self.beta = arguments['beta']
        
    def forward(self):
        a = gamma.rvs(self.k, self.theta)
        return beta.rvs(a, self.beta)