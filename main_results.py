##################################################################
###Work developed by Luis Dias | e-mail:luis.m.dias@inesctec.pt###
##################################################################

#Required libraries
import time
import sys
sys.path.insert(1, 'src/') #point to the required folder
from sensitivity_analysis import * #import the required library for the main

#Start clock
start_time = time.time()

#Definition of the main command lines to be executed in order to perform the sensitivity analysis
if __name__ == '__main__':

    #Test function
    monitoring_bias = int(sys.argv[1])/100
    short_term = Failure_mode_degradation(initial_condition = 0, failure_threshold = 500, average_degradation_parameter = 25, variability_degradation_parameter = 30,
                                          degradation = [], inspection = 15, time_maintenance_threshold = 100, condition_maintenance_threshold = 500, inspection_costs = 0, sensor_costs = 0,
                                          preventive_maintenance_costs= 30, corrective_maintenance_costs = 60, uncertainty_bias = monitoring_bias, uncertainty_level = 0.10) #short-term failure mode definition
    long_term = Failure_mode_degradation(initial_condition = 0, failure_threshold = 1000, average_degradation_parameter = 4.443, variability_degradation_parameter = 2.657,
                                     degradation = [], inspection = 15, time_maintenance_threshold = 200, condition_maintenance_threshold = 1000, inspection_costs = 1, sensor_costs = 5,
                                     preventive_maintenance_costs= 500, corrective_maintenance_costs = 750, uncertainty_bias = monitoring_bias, uncertainty_level = 0.10) #long-term failure mode definition
    shock_threshold = 250 #threshold of activation for the shocks
    lameda_shocks = int(sys.argv[2])/10 #shocks per time step
    shock_intensity_mean = 30 #normal distribution
    shock_intensity_stdev = 20 #normal distribution

    #maintenance_policy_list = [sys.argv[3]] #maintenance policy to analyze
    maintenance_policy_list = ['TBM','CBM','ECBM'] #maintenance policy to analyze ICBM
    simulating_periods = int(sys.argv[4]) #simulating periods for our problem
    policy_limit = long_term.failure_threshold #policy limit
    policy_step = int(sys.argv[5]) #policy precision for the optimal decision
    ratio_limit = 25 #ratio maximum value that is going to be used for the study
    sensitivity_step = 1 #ratio delta increment for the study
    results_suffix = f'{simulating_periods}sim_{policy_step}polstep_{int(lameda_shocks*10)}shocks_bias_{int(monitoring_bias*100)}' #results naming
    sensitivity_case = sys.argv[6] #sensitivity analysis type to be performed

    #check if the inputed maintenance policy is valid
    if sys.argv[3] not in allowed_maintenance_policy_list:
        print(f'The inputed maintenance policy {sys.argv[3]} is not valid! Choose a policy from the following list: {allowed_maintenance_policy_list}')
        sys.exit()

    #Run the specified analysis
    if sensitivity_case == '1':
        print(f"Analyze MTBF ratio for {simulating_periods} simulating periods and a maintenance policy step of {policy_step}!")
        #function mtbf ratio
        results = failure_modes_mtbf_ratio(long_term, short_term, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, ratio_limit, sensitivity_step)
        results.to_csv(f'results/mtbf_ratio_results_{results_suffix}.csv')

        #plot results
        plot_sensitivity_analysis_results(results, 'MTBF ratio', 'Scaled expected cost')

    elif sensitivity_case == '2':
        print(f"Analyze shocks duration ratio for {simulating_periods} simulating periods and a maintenance policy step of {policy_step}!")
        #function shocks ratio
        results = failure_modes_shock_ratio(long_term, short_term, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, ratio_limit, sensitivity_step)
        results.to_csv(f'results/shocks_ratio_results_{results_suffix}.csv')

        #plot results
        plot_sensitivity_analysis_results(results, 'Shock ratio', 'Scaled expected cost')

    elif sensitivity_case == '3':
        print(f"Analyze shocks intensity ratio for {simulating_periods} simulating periods and a maintenance policy step of {policy_step}!")
        #function shocks intensity ratio
        results = failure_modes_shocks_intensity(long_term, short_term, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, ratio_limit, sensitivity_step)
        results.to_csv(f'results/shocks_intensity_ratio_results_{results_suffix}.csv')

        #plot results
        plot_sensitivity_analysis_results(results, 'Shock intentisity ratio', 'Scaled expected cost')

    elif sensitivity_case == '4':
        print(f"Analyze maintenance costs ratio for {simulating_periods} simulating periods and a maintenance policy step of {policy_step}!")
        #function costs ratio
        results = failure_modes_maintenance_costs_ratio(long_term, short_term, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, ratio_limit, sensitivity_step)
        results.to_csv(f'results/maintenance_costs_ratio_results_{results_suffix}.csv')

        #plot results
        plot_sensitivity_analysis_results(results, 'Maintenance costs ratio', 'Scaled expected cost')

    elif sensitivity_case == '5':
        print(f"Analyze monitoring costs ratio for {simulating_periods} simulating periods and a maintenance policy step of {policy_step}!")
        #function monitoring costs ratio
        results = failure_modes_condition_costs(long_term, short_term, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, ratio_limit, sensitivity_step)
        results.to_csv(f'results/monitoring_costs_ratio_results_{results_suffix}.csv')

        #plot results
        plot_sensitivity_analysis_results(results, 'Monitoring costs ratio', 'Scaled expected cost')

    elif sensitivity_case == '6':
        print(f"Analyze monitoring costs ratio for {simulating_periods} simulating periods and a maintenance policy step of {policy_step}!")
        #function monitoring costs ratio
        results = maintenance_to_condition_costs(long_term, short_term, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, ratio_limit, sensitivity_step)
        results.to_csv(f'results/monitoring_to_maintenance_costs_ratio_results_{results_suffix}.csv')

        #plot results
        plot_sensitivity_analysis_results(results, 'Monitoring vs maintenance costs ratio', 'Scaled expected cost')

    elif sensitivity_case == '7':
        print(f"Analyze error level for {simulating_periods} simulating periods and a maintenance policy step of {policy_step}!")
        #function monitoring costs ratio
        results = failure_modes_monitoring_error(long_term, short_term, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, ratio_limit, sensitivity_step)
        results.to_csv(f'results/monitoring_error_results_{results_suffix}.csv')

        #plot results
        plot_sensitivity_analysis_results(results, 'Monitoring error level', 'Scaled expected cost')

    else:
        print("Choose one of the following options to perform the intended sensitivity analysis {1,2,3,4,5, 6 or 7}!")

    #compute computational runtime
    computed_time = round((time.time() - start_time),2)
    with open("runs_computational_time.txt", "a") as file_object:
        file_object.write(f"{sensitivity_case}--- Results computational time = {computed_time} seconds for {results_suffix} ---\n")