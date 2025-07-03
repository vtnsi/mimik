# -*- coding: utf-8 -*-
"""
Created on Mon May 12 11:27:06 2025

Task classes for MIMIK tutorial

"""

from scipy.stats import beta, lognorm

from mimik.component_graph.abstract_task import AbstractTask


class FindTask(AbstractTask):
    
    def __init__(self, arguments: dict):
        '''
        Initialize custom Find task

        Parameters
        ----------
        arguments : dict
            dictionary of arguments
        '''
        
        super().__init__("FindTask", arguments)
        self.mu = arguments['mu']
        self.sigma2 = arguments['sigma2']
        self.alpha = arguments['alpha']
        
    def forward(self):
        b = lognorm.rvs(self.sigma2, self.mu)
        return beta.rvs(self.alpha, b)