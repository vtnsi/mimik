# -*- coding: utf-8 -*-
"""

killchain analysis using MIMIK
assume a beta Bernoulli model

"""

import os

from mimik.killweb import Killweb


# config filename
config_filename = "killchain_betabernoulli.json"

# number of simulation runs
N = 1000

def main():
    
    # load killchain
    configs_pth = os.path.join('configs', config_filename)
    killchain = Killweb(config_file = configs_pth)
    killchain.create_component_networkx_visualization()
    
    # MC Sim
    killchain.monte_carlo_on_paths(N)
    print(" ")
    print("Monte Carlo Simulation")
    killchain.print_probabilities_of_paths()
    
    # calculate variance of MC simulation results
    path = killchain.get_all_paths_in_killweb()[0]
    sigma2 = killchain.component_metrics.calculate_variance(path)
    print("Variance: ", sigma2)
    
    # plot MC distribution
    killchain.plot_monte_carlo_distribution(path)
    
    
if __name__ == "__main__":
    main()