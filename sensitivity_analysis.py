####################################################
###Funções dedicadas à análise de sensibilidade  ###
####################################################

#Required libraries
import sys
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
    ratio_interval = [ratio for ratio in range(1,upper_limmit,int(sensitivity_step*upper_limmit))]
    ratio_interval.append(upper_limmit) #garantuee that we add the maximum allowed value for the ratio

    #Compute the new drift parameter (wienner process for the short-term) given the specified values of the ratio and predefined parameters
    lt_mtbf = lt_failure_mode.compute_mtbf('gamma')

    #Dataframe to save the results
    agregated_results = pd.DataFrame({"mtbf_ratio": ratio_interval})

    #scale the ratio values
    agregated_results['mtbf_ratio'] = agregated_results['mtbf_ratio'] / upper_limmit

    #analyze the process for each maintenance policy that we have available
    for maintenance_policy in maintenance_policy_list:
        #define the variabless that will save the results of interest
        optimal_cost = list()

        #analyse a given ratio value
        for ratio in agregated_results.iloc[:, 0]:

            #output progress
            print(f'{maintenance_policy} - The mtbf ratio value between the short-term and long-term failure is R={ratio}')

            #Calcular o drift que precisamos dado o rácio e mantendo o resto da informação (temos que ajustar o ratio para a escala real)
            st_failure_mode.average_degradation_parameter = (st_failure_mode.failure_threshold-st_failure_mode.initial_condition)/(ratio * lt_mtbf)

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
    ratio_interval = [ratio for ratio in range(1,upper_limmit,int(sensitivity_step*upper_limmit))]
    ratio_interval.append(upper_limmit) #garantue that we add the maximum allowed value for the ratio

    #Dataframe to save the results
    agregated_results = pd.DataFrame({"shocks_ratio": ratio_interval})

    #scale the ratio values
    agregated_results['shocks_ratio'] = agregated_results['shocks_ratio'] / upper_limmit

    #analyze the process for each maintenance policy that we have available
    for maintenance_policy in maintenance_policy_list:
        #define the variabless that will save the results of interest
        optimal_cost = list()

        #analyse a given ratio value
        for ratio in agregated_results.iloc[:, 0]:

            #output progress
            print(f'{maintenance_policy} - The mtbf ratio value between the short-term and long-term failure is R={ratio}')

            #compute the new shock threshold based on the specified ratio
            new_shock_threshold = st_failure_mode.failure_threshold * ratio

            #Simular a política de manutenção pretendida e guardar o melhor resultado
            cost = scaled_maintenance_policy_optimal_cost(lt_failure_mode, st_failure_mode, new_shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)

            #save the obtained results
            optimal_cost.append(cost)

        #return the results in a pandas dataframe
        agregated_results[f"optimal_cost_{maintenance_policy}"] = optimal_cost

    #final table
    return agregated_results

#Study the maintenance costs ratio between the short-term failure and long-term failure (Ratio = st_costs/lt_costs)
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
def failure_modes_maintenance_costs_ratio(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, sensitivity_step):

    #define the shock ratio between the time between shocks and the short-term failure mode mtbf
    upper_limmit = 100 #define value scale dado que o range não aceia floats
    ratio_interval = [ratio for ratio in range(1,upper_limmit,int(sensitivity_step*upper_limmit))]
    ratio_interval.append(upper_limmit) #garantue that we add the maximum allowed value for the ratio

    #Dataframe to save the results
    agregated_results = pd.DataFrame({"costs_ratio": ratio_interval})

    #scale the ratio values
    agregated_results['costs_ratio'] = agregated_results['costs_ratio'] / upper_limmit

    #original costs
    st_preventive_maintenance_costs, st_corrective_maintenance_costs = st_failure_mode.preventive_maintenance_costs, st_failure_mode.corrective_maintenance_costs

    #analyze the process for each maintenance policy that we have available
    for maintenance_policy in maintenance_policy_list:
        #analyse the costs given its type (corrective or preventive)
        for costs_type in ['preventive','corrective']:
            #define the variabless that will save the results of interest
            optimal_cost = list()
            #analyse a given ratio value
            for ratio in agregated_results.iloc[:, 0]:

                #output progress
                print(f'{maintenance_policy} - The costs ratio value between the short-term and long-term failure is R={ratio}')

                #compute the new costs threshold based on the specified ratio
                if costs_type == 'preventive':
                    st_failure_mode.preventive_maintenance_costs = lt_failure_mode.preventive_maintenance_costs * ratio
                else:
                    st_failure_mode.corrective_maintenance_costs = lt_failure_mode.corrective_maintenance_costs * ratio

                #Simular a política de manutenção pretendida e guardar o melhor resultado
                cost = scaled_maintenance_policy_optimal_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)

                #save the obtained results
                optimal_cost.append(cost)

                #always reset the costs to the original value for safety
                if costs_type == 'preventive':
                    st_failure_mode.preventive_maintenance_costs = st_preventive_maintenance_costs
                else:
                    st_failure_mode.corrective_maintenance_costs = st_corrective_maintenance_costs

            #return the results in a pandas dataframe
            agregated_results[f"optimal_cost_{costs_type}_{maintenance_policy}"] = optimal_cost

    #final table
    return agregated_results

#Study the shocks intensity ratio between the expected degradation with shocks and without shocks (Ratio = (delta+shocks_delta)/delta)
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
def failure_modes_shocks_intensity(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, sensitivity_step):

    #define the mtbf ratio that we want to study
    upper_limit = 10 #define value scale dado que o range não aceia floats
    ratio_interval = [ratio for ratio in range(1,upper_limit,sensitivity_step)]
    ratio_interval.append(upper_limit) #garantuee that we add the maximum allowed value for the ratio

    #Compute the average degradation given the long-term failure mode MTBF and the failure threshold
    average_delta = lt_failure_mode.compute_mtbf('wienner')/lt_failure_mode.failure_threshold

    #Dataframe to save the results
    agregated_results = pd.DataFrame({"shock_intensity_ratio": ratio_interval})

    #analyze the process for each maintenance policy that we have available
    for maintenance_policy in maintenance_policy_list:
        #define the variabless that will save the results of interest
        optimal_cost = list()

        #analyse a given ratio value
        for ratio in ratio_interval:

            #output progress
            print(f'{maintenance_policy} - The ratio value between the degradation with shocks and the average degradation is R={ratio}')

            #Calcular o drift que precisamos dado o rácio e mantendo o resto da informação (temos que ajustar o ratio para a escala real)
            shock_intensity_mean = ratio * average_delta - average_delta

            #Simular a política de manutenção pretendida e guardar o melhor resultado
            cost = scaled_maintenance_policy_optimal_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)

            #save the obtained results
            optimal_cost.append(cost)

        #return the results in a pandas dataframe
        agregated_results[f"optimal_cost_{maintenance_policy}"] = optimal_cost

    #final table
    return agregated_results

#Study the inspection costs ratio between the inspection cost and the monitoring cost (Ratio = monitoring_cost/inspection_cost)
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
def failure_modes_condition_costs(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, sensitivity_step):

    #define the mtbf ratio that we want to study
    upper_limit = 10 #define value scale dado que o range não aceia floats
    ratio_interval = [ratio for ratio in range(1,upper_limit,sensitivity_step)]
    ratio_interval.append(upper_limit) #garantuee that we add the maximum allowed value for the ratio

    #Dataframe to save the results
    agregated_results = pd.DataFrame({"condition_costs_ratio": ratio_interval})

    #analyze the process for each maintenance policy that we have available
    for maintenance_policy in maintenance_policy_list:
        #define the variabless that will save the results of interest
        optimal_cost = list()

        #analyse a given ratio value
        for ratio in ratio_interval:

            #output progress
            print(f'{maintenance_policy} - The ratio value between the sensor cost and the inspection cost is R={ratio}')

            #Calcular o custo do sensor com base no custo de inspeção definido
            st_failure_mode.sensor_costs = ratio * st_failure_mode.inspection_costs
            lt_failure_mode.sensor_costs = ratio * lt_failure_mode.inspection_costs

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

    #Scale results according to the maintenance policy
    if maintenance_policy== 'ICBM':
        cost = 9999999 #really high value
        for inspection_time in range(1,policy_limit,policy_step):
            st_failure_mode.inspection, lt_failure_mode.inspection = inspection_time, inspection_time #test different inspection times for the inspection based condition based maintenance
            #simulate the process
            _, computed_cost, _ = optimal_maintenance_policy_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)
            #check if we update the results
            if computed_cost < cost:
                cost = computed_cost #new best cost
    #in case we use another maintenance policy
    else:
        _, cost, _ = optimal_maintenance_policy_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)

    #min max scaling
    if cost < best_cost:#just to check if everything is working according to the expected theory
        print(f'Cost={cost} and bescost={best_cost} and worstcost={worst_cost}')
    return (cost-best_cost)/(worst_cost-best_cost)

#Plot the results according to the paper format
#Parameters:
#sensitivity_results - Provide the pandas dataframe with the results
#x_axis_name - X axis label name
#y_axis_name - Y axis label name
def plot_sensitivity_analysis_results(sensitivity_results, x_axis_name, y_axis_name):

    ##build inspection policy
    fig, ax = plt.subplots(figsize=(20, 10))

    #plot the results for the required maintenance policies
    for col in sensitivity_results.iloc[:, 1:].columns:
        ax.plot(sensitivity_results[sensitivity_results.columns[0]], sensitivity_results[col], label = col)

    #Plot labeling
    ax.set(xlabel=x_axis_name, ylabel=y_axis_name)

    #add thresholds
    ax.plot(sensitivity_results.iloc[:, 0], np.array([1] * len(sensitivity_results.index)), label = 'Corrective_maintenance')

    #Plot ylim assuming the scaled values
    plt.ylim(0, 1.05)

    #Show results
    plt.legend(loc='upper left')
    plt.show()

#Definition of the main command lines to be executed in order to perform the sensitivity analysis
if __name__ == '__main__':

    #Test function
    short_term = Failure_mode_degradation(initial_condition = 10, failure_threshold = 100, average_degradation_parameter = 2, variability_degradation_parameter = 4,
                                          degradation = [], inspection = 15, time_maintenance_threshold = 100, condition_maintenance_threshold = 100, inspection_costs = 5, sensor_costs = 25, preventive_maintenance_costs= 100, corrective_maintenance_costs = 200) #short-term failure mode definition
    long_term = Failure_mode_degradation(initial_condition = 0, failure_threshold = 200, average_degradation_parameter = 0.5, variability_degradation_parameter = 2,
                                         degradation = [], inspection = 15, time_maintenance_threshold = 200, condition_maintenance_threshold = 200, inspection_costs = 0, sensor_costs = 0, preventive_maintenance_costs= 500, corrective_maintenance_costs = 1000) #long-term failure mode definition
    shock_threshold = 50 #threshold of activation for the shocks
    lameda_shocks = 0.5 #shocks per time step
    shock_intensity_mean = 3 #normal distribution
    shock_intensity_stdev = 2 #normal distribution
    simulating_periods = 10000 #simulating periods for our problem
    maintenance_policy_list = ['TBM','CBM'] #'ICBM','CBM'
    policy_limit = 200 #policy limit
    policy_step = 5
    sensitivity_step = 0.1

    #Run the specified analysis
    if sys.argv[1]== '1':
        print("Analyze MTBF ratio!")
        #function mtbf ratio
        results = failure_modes_mtbf_ratio(long_term, short_term, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, sensitivity_step)
        results.to_csv('mtbf_ratio_results.csv')

        #plot results
        plot_sensitivity_analysis_results(results, 'MTBF ratio', 'Scaled expected cost')

    elif sys.argv[1]== '2':
        print("Analyze shocks duration ratio!")
        #function shocks ratio
        results = failure_modes_shock_ratio(long_term, short_term, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, sensitivity_step)
        results.to_csv('shocks_ratio_results.csv')

        #plot results
        plot_sensitivity_analysis_results(results, 'Shock ratio', 'Scaled expected cost')

    elif sys.argv[1]== '3':
        print("Analyze shocks intensity ratio!")
        #function shocks intensity ratio
        results = failure_modes_shocks_intensity(long_term, short_term, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, sensitivity_step=1)
        results.to_csv('shocks_intensity_ratio_results.csv')

        #plot results
        plot_sensitivity_analysis_results(results, 'Shock intentisity ratio', 'Scaled expected cost')

    elif sys.argv[1]== '4':
        print("Analyze maintenance costs ratio!")
        #function costs ratio
        results = failure_modes_maintenance_costs_ratio(long_term, short_term, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, sensitivity_step)
        results.to_csv('maintenance_costs_ratio_results.csv')

        #plot results
        plot_sensitivity_analysis_results(results, 'Maintenance costs ratio', 'Scaled expected cost')

    elif sys.argv[1]== '5':
        print("Analyze monitoring costs ratio!")
        #function monitoring costs ratio
        results = failure_modes_condition_costs(long_term, short_term, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, sensitivity_step=1)
        results.to_csv('monitoring_costs_ratio_results.csv')

        #plot results
        plot_sensitivity_analysis_results(results, 'Monitoring costs ratio', 'Scaled expected cost')
    else:
        print("Choose one of the following options to perform the intended sensitivity analysis {1,2,3,4 or 5}!")

