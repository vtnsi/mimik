# -*- coding: utf-8 -*-
"""
Created on Mon May 12 11:27:06 2025

Task classes for MIMIK tutorial

"""

from scipy.stats import beta

from mimik.component_graph.abstract_task import AbstractTask


class BetaBernoulli(AbstractTask):
    '''
    Class for the beta Bernoulli prior
    '''
    
    def __init__(self, arguments: dict):
        '''
        Initialize custom BetaBernoulli task

        Parameters
        ----------
        arguments : dict
            dictionary of arguments
        '''
        
        super().__init__("BetaBernoulli", arguments)
        self.alpha = arguments['alpha']
        self.beta = arguments['beta']
        
    def forward(self):
        return beta.rvs(self.alpha, self.beta)