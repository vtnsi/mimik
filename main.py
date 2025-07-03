import os
import argparse
from mimik.killweb import Killweb


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='MIMIK', usage='%(prog)s [options]')
    parser.add_argument('-s', '--silent', action="store_true")
    args = parser.parse_args()
    killweb = Killweb(
        working_dir="./examples/0_minimal_example",
        config_file=os.path.join(
            ".", "examples", "0_minimal_example", "configs", "minimal_example.json"
        ),
       silent=args.silent
    )
    # killweb = Killweb(
    #     working_dir="./examples/1_long_range_strikes_example",
    #     config_file=os.path.join(
    #         ".", "examples", "1_long_range_strikes_example", "configs", "killweb_interconnected.json"
    #     ),
    #     silent=args.silent
    # )
    # killweb = Killweb(
    #     working_dir="./examples/2_top_gun_maverick_example",
    #     config_file=os.path.join(
    #         ".", "examples", "2_top_gun_maverick_example", "configs", "top_gun_maverick_config.json"
    #     ),
    #     silent=args.silent
    # )

    killweb.create_component_networkx_visualization()

    # NOTE The following code block is reserved for 1_long_range_strikes_example. Please reference the examples directory for how to run the 2_top_gun_maverick_example.
    # new_component_dict = {"task": "Track", "task_arguments": {"alpha_track": 125, "beta_track": 7, "tau": 10}, "system_name": "System_4"}
    # killweb.add_new_component(
    #     component_name="Track_Algorithm_4",
    #     to_components=["Equation_2", "Equation_3"],
    #     from_components=["Sensor_2"],
    #     component_attributes=new_component_dict
    # )
    # killweb.create_component_networkx_visualization()
    # killweb.print_nodes()
    # killweb.print_edges()
    # killweb.print_all_paths_in_killweb()
    # killweb.monte_carlo_on_paths(100)
    # killweb.print_probabilities_of_paths(5)

    # killweb.save_killweb_to_config_file(os.path.join(".", "examples", "1_long_range_strikes_example", "output", "saved_interconnected.json"), "better_track")

    # path_to_test = ["Radar_2", "Sensor_2", "Track Algorithm_1", "Equation_1", "Missle_1", "Personnel_1"]
    # killweb.print_proportion_complete(path_to_test)
    # killweb.print_average_number_of_successes(path_to_test)
    # killweb.print_variance(path_to_test)
    # killweb.plot_monte_carlo_distribution(path_to_test)
    # killweb.calculate_node_centrality()
