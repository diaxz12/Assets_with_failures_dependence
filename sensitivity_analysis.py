####################################################
###Funções dedicadas à análise de sensibilidade  ###
####################################################

#Required libraries
from Asset_degradation import *

#Study the MTBF ratio between the short-term failure and long-term failure (Ratio = MTBF_st/MTBF_lt)
#Parameters:
#lt_failure_mode - Long term failure mode object that is used for the degradation process
#st_failure_mode - Short term failure mode object that is used for the degradation process
#shock_threshold - Shock threshold
#shock_lameda - Poisson arrival rate for the shock process
#shock_mean - Normal distribution mean parameter
#shock_stdev - Normal distribution standard deviation parameter
#number_periods - Number of time periods that are used for the simulation
#maintenance_policy_list - Compute the costs according to the defined maintenance policy list (CM - corrective maintenance, PM - perfect maintenance, TBM - time based maintenance, ICBM - with perfect inspection, CBM - with perfect continuous monitoring, EICBM - with imperfect inspection, ECBM - with imperfect continuous monitoring)
#policy_iteration_limit - Limit to where we can iteratively study the respective maintenance policy
#policy_step - Number of times that we want to make a step (by default it takes the unit value)
#sensitivity_step - The iterative step that we want when going through the interval
def failure_modes_mtbf_ratio(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, sensitivity_step):

    #define the mtbf ratio that we want to study
    upper_limmit = 100 #define value scale dado que o range não aceia floats
    mtbf_ratio_interval = [ratio for ratio in range(1,upper_limmit,int(sensitivity_step*upper_limmit))]
    mtbf_ratio_interval.append(upper_limmit) #garantuee that we add the maximum allowed value for the ratio

    #Compute the new drift parameter (wienner process for the short-term) given the specified values of the ratio and predefined parameters
    lt_mtbf = lt_failure_mode.compute_mtbf('gamma')

    #Dataframe to save the results
    agregated_results = pd.DataFrame({"mtbf_ratio": mtbf_ratio_interval})

    #scale the ratio values
    agregated_results['mtbf_ratio'] = agregated_results['mtbf_ratio'] / upper_limmit

    #analyze the process for each maintenance policy that we have available
    for maintenance_policy in maintenance_policy_list:
        #define the variabless that will save the results of interest
        optimal_cost = list()

        #analyse a given ratio value
        for ratio in mtbf_ratio_interval:

            #output progress
            print(f'{maintenance_policy} - The mtbf ratio value between the short-term and long-term failure is R={ratio}')

            #Calcular o drift que precisamos dado o rácio e mantendo o resto da informação (temos que ajustar o ratio para a escala real)
            st_failure_mode.average_degradation_parameter = (st_failure_mode.failure_threshold-st_failure_mode.initial_condition)/(ratio/upper_limmit * lt_mtbf)

            #Simular a política de manutenção pretendida e guardar o melhor resultado
            cost = scaled_maintenance_policy_optimal_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)

            #save the obtained results
            optimal_cost.append(cost)

        #return the results in a pandas dataframe
        agregated_results[f"optimal_cost_{maintenance_policy}"] = optimal_cost

    #final table
    return agregated_results

#Study the MTBF ratio between the short-term failure and long-term failure (Ratio = MTBF_st/MTBF_lt)
#Parameters:
#lt_failure_mode - Long term failure mode object that is used for the degradation process
#st_failure_mode - Short term failure mode object that is used for the degradation process
#shock_threshold - Shock threshold
#shock_lameda - Poisson arrival rate for the shock process
#shock_mean - Normal distribution mean parameter
#shock_stdev - Normal distribution standard deviation parameter
#number_periods - Number of time periods that are used for the simulation
#maintenance_policy_list - Compute the costs according to the defined maintenance policy list (CM - corrective maintenance, PM - perfect maintenance, TBM - time based maintenance, ICBM - with perfect inspection, CBM - with perfect continuous monitoring, EICBM - with imperfect inspection, ECBM - with imperfect continuous monitoring)
#policy_iteration_limit - Limit to where we can iteratively study the respective maintenance policy
#policy_step - Number of times that we want to make a step (by default it takes the unit value)
#sensitivity_step - The iterative step that we want when going through the interval
def failure_modes_shock_ratio(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, sensitivity_step):

    #define the shock ratio between the time between shocks and the short-term failure mode mtbf
    upper_limmit = 100 #define value scale dado que o range não aceia floats
    shock_ratio_interval = [ratio for ratio in range(1,upper_limmit,int(sensitivity_step*upper_limmit))]
    shock_ratio_interval.append(upper_limmit) #garantue that we add the maximum allowed value for the ratio

    #Dataframe to save the results
    agregated_results = pd.DataFrame({"shocks_ratio": shock_ratio_interval})

    #scale the ratio values
    agregated_results['shocks_ratio'] = agregated_results['shocks_ratio'] / upper_limmit

    #analyze the process for each maintenance policy that we have available
    for maintenance_policy in maintenance_policy_list:
        #define the variabless that will save the results of interest
        optimal_cost = list()

        #analyse a given ratio value
        for ratio in shock_ratio_interval:

            #output progress
            print(f'{maintenance_policy} - The mtbf ratio value between the short-term and long-term failure is R={ratio}')

            #compute the new shock threshold based on the specified ratio
            shock_threshold = st_failure_mode.failure_threshold*ratio

            #Simular a política de manutenção pretendida e guardar o melhor resultado
            cost = scaled_maintenance_policy_optimal_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)

            #save the obtained results
            optimal_cost.append(cost)

        #return the results in a pandas dataframe
        agregated_results[f"optimal_cost_{maintenance_policy}"] = optimal_cost

    #final table
    return agregated_results

#Scale the values according to the best and worst possible result
def scaled_maintenance_policy_optimal_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step):

    #Worst possible result
    _, worst_cost, _ = optimal_maintenance_policy_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, 'CM', policy_limit, policy_step)
    _, best_cost, _ = optimal_maintenance_policy_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, 'PM', policy_limit, policy_step)

    #Scale results
    _, cost, _ = optimal_maintenance_policy_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)

    #min max scaling
    return (cost-best_cost)/(worst_cost-best_cost)


#Plot the results according to the paper format
#Parameters:
#sensitivity_results - Provide the pandas dataframe with the results
#x_axis_name - X axis label name
#y_axis_name - Y axis label name
def plot_sensitivity_analysis_results(maintenance_policy_list, sensitivity_results, x_axis_name, y_axis_name):

    ##build inspection policy
    fig, ax = plt.subplots(figsize=(20, 10))

    #plot the results for the required maintenance policies
    for maintenance_policy in maintenance_policy_list:
        ax.plot(sensitivity_results[sensitivity_results.columns[0]], sensitivity_results[f'optimal_cost_{maintenance_policy}'], label = maintenance_policy)

    #Plot labeling
    ax.set(xlabel=x_axis_name, ylabel=y_axis_name)

    #add thresholds
    ax.plot(sensitivity_results[sensitivity_results.columns[0]], np.array([1] * len(sensitivity_results.index)), label = 'Corrective_maintenance')

    #Plot ylim assuming the scaled values
    plt.ylim(0, 1.05)

    #Show results
    plt.legend(loc='upper left')
    plt.show()

#Test function
short_term = Failure_mode_degradation(initial_condition = 10, failure_threshold = 100, average_degradation_parameter = 2, variability_degradation_parameter = 4,
                                      degradation = [], inspection = 15, time_maintenance_threshold = 100, condition_maintenance_threshold = 100, inspection_costs = 10, preventive_maintenance_costs= 100, corrective_maintenance_costs = 200) #short-term failure mode definition
long_term = Failure_mode_degradation(initial_condition = 0, failure_threshold = 200, average_degradation_parameter = 0.1, variability_degradation_parameter = 2,
                                     degradation = [], inspection = 15, time_maintenance_threshold = 200, condition_maintenance_threshold = 200, inspection_costs = 10, preventive_maintenance_costs= 200, corrective_maintenance_costs = 1000) #long-term failure mode definition
shock_threshold = 50 #threshold of activation for the shocks
lameda_shocks = 0.5 #shocks per time step
shock_intensity_mean = 7 #normal distribution
shock_intensity_stdev = 2 #normal distribution
simulating_periods = 10000
maintenance_policy_list = ['TBM','CBM']
policy_limit = 200
policy_step = 10
sensitivity_step = 0.1


#function mtbf ratio
results = failure_modes_mtbf_ratio(long_term, short_term, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, sensitivity_step)
results.to_csv('mtbf_ratio_results.csv')

#plot results
plot_sensitivity_analysis_results(maintenance_policy_list, results, 'MTBF ratio', 'Scaled expected cost')

#function shocks ratio
results = failure_modes_shock_ratio(long_term, short_term, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, sensitivity_step)
results.to_csv('shocks_ratio_results.csv')

#plot results
plot_sensitivity_analysis_results(maintenance_policy_list, results, 'Shock ratio', 'Scaled expected cost')