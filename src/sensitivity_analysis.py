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
#ratio_limit - Defines the ratio maximum value that is going to be used for the study
#sensitivity_step - The iterative step that we want when going through the interval
def failure_modes_mtbf_ratio(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, ratio_limit, sensitivity_step):

    #define the mtbf ratio that we want to study
    ratio_interval = [ratio for ratio in range(1,ratio_limit,sensitivity_step)]
    ratio_interval.append(ratio_limit) #garantuee that we add the maximum allowed value for the ratio

    #Compute the new drift parameter (wienner process for the short-term) given the specified values of the ratio and predefined parameters
    lt_mtbf = lt_failure_mode.compute_mtbf('gamma')

    #Dataframe to save the results
    agregated_results = pd.DataFrame({"mtbf_ratio": ratio_interval})

    #analyze the process for each maintenance policy that we have available
    for maintenance_policy in maintenance_policy_list:

        #define the variabless that will save the results of interest
        optimal_decision, optimal_cost, optimal_lifetime = list(), list(), list()

        #analyse a given ratio value
        for ratio in agregated_results.iloc[:, 0]:

            #output progress
            print(f'{maintenance_policy} - The mtbf ratio value between the short-term and long-term failure is R={ratio}')

            #Calcular o drift que precisamos dado o rácio e mantendo o resto da informação (temos que ajustar o ratio para a escala real)
            st_failure_mode.average_degradation_parameter = (st_failure_mode.failure_threshold-st_failure_mode.initial_condition) * ratio / lt_mtbf

            #Simular a política de manutenção pretendida e guardar o melhor resultado
            decision, cost, lifetimes = scaled_maintenance_policy_optimal_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)

            #save the obtained results
            optimal_decision.append(decision), optimal_cost.append(cost), optimal_lifetime.append(lifetimes)

        #return the results in a pandas dataframe
        agregated_results[f"optimal_decision_{maintenance_policy}"] = optimal_decision
        agregated_results[f"optimal_cost_{maintenance_policy}"] = optimal_cost
        agregated_results[f"optimal_lifetime_{maintenance_policy}"] = optimal_lifetime

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
#ratio_limit - Defines the ratio maximum value that is going to be used for the study
#sensitivity_step - The iterative step that we want when going through the interval
def failure_modes_shock_ratio(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, ratio_limit, sensitivity_step):

    #define the shock ratio between the time between shocks and the short-term failure mode mtbf
    ratio_interval = [ratio for ratio in range(1,ratio_limit,sensitivity_step)]
    ratio_interval.append(ratio_limit) #garantue that we add the maximum allowed value for the ratio

    #Dataframe to save the results
    agregated_results = pd.DataFrame({"shocks_ratio": ratio_interval})

    #analyze the process for each maintenance policy that we have available
    for maintenance_policy in maintenance_policy_list:
        #define the variabless that will save the results of interest
        optimal_decision, optimal_cost, optimal_lifetime = list(), list(), list()

        #analyse a given ratio value
        for ratio in agregated_results.iloc[:, 0]:

            #output progress
            print(f'{maintenance_policy} - The mtbf ratio value between the short-term and long-term failure is R={ratio}')

            #compute the new shock threshold based on the specified ratio
            new_shock_threshold = st_failure_mode.failure_threshold / ratio

            #Simular a política de manutenção pretendida e guardar o melhor resultado
            decision, cost, lifetimes = scaled_maintenance_policy_optimal_cost(lt_failure_mode, st_failure_mode, new_shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)

            #save the obtained results
            optimal_decision.append(decision), optimal_cost.append(cost), optimal_lifetime.append(lifetimes)

        #return the results in a pandas dataframe
        agregated_results[f"optimal_decision_{maintenance_policy}"] = optimal_decision
        agregated_results[f"optimal_cost_{maintenance_policy}"] = optimal_cost
        agregated_results[f"optimal_lifetime_{maintenance_policy}"] = optimal_lifetime

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
#ratio_limit - Defines the ratio maximum value that is going to be used for the study
#sensitivity_step - The iterative step that we want when going through the interval
def failure_modes_maintenance_costs_ratio(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, ratio_limit, sensitivity_step):

    #define the shock ratio between the time between shocks and the short-term failure mode mtbf
    ratio_interval = [ratio for ratio in range(1,ratio_limit,sensitivity_step)]
    ratio_interval.append(ratio_limit) #garantue that we add the maximum allowed value for the ratio

    #Dataframe to save the results
    agregated_results = pd.DataFrame({"costs_ratio": ratio_interval})

    #original costs (we assume that is installed for the long-term failure!)
    original_monitoring_equipment_cost, original_inspection_cost = lt_failure_mode.sensor_costs, lt_failure_mode.inspection_costs
    st_corrective_maintenance_costs, st_preventive_maintenance_costs = st_failure_mode.corrective_maintenance_costs, st_failure_mode.preventive_maintenance_costs
    lt_corrective_maintenance_costs, lt_preventive_maintenance_costs = lt_failure_mode.corrective_maintenance_costs, lt_failure_mode.preventive_maintenance_costs

    #compute the original ratio
    st_corrective_maintenance_ratio = st_failure_mode.corrective_maintenance_costs / st_preventive_maintenance_costs
    inspection_monitoring_ratio, equipment_monitoring_ratio = lt_failure_mode.corrective_maintenance_costs / lt_failure_mode.inspection_costs, lt_failure_mode.corrective_maintenance_costs / lt_failure_mode.sensor_costs

    #analyze the process for each maintenance policy that we have available
    for maintenance_policy in maintenance_policy_list:
        #analyse the costs given its type (corrective or preventive)
        for costs_type in ['preventive','corrective']:
            #define the variabless that will save the results of interest
            optimal_decision, optimal_cost, optimal_lifetime = list(), list(), list()
            #analyse a given ratio value
            for ratio in agregated_results.iloc[:, 0]:

                #output progress
                print(f'{maintenance_policy} - The costs ratio value between the short-term and long-term failure is R={ratio}')

                #compute the new costs threshold based on the specified ratio
                if costs_type == 'preventive':
                    st_failure_mode.preventive_maintenance_costs = lt_failure_mode.preventive_maintenance_costs / ratio
                    st_failure_mode.corrective_maintenance_costs = st_failure_mode.preventive_maintenance_costs * st_corrective_maintenance_ratio
                else:
                    st_failure_mode.corrective_maintenance_costs = lt_failure_mode.corrective_maintenance_costs / ratio
                    st_failure_mode.preventive_maintenance_costs = st_failure_mode.corrective_maintenance_costs / st_corrective_maintenance_ratio

                #Adjust the inspection costs and sensor costs accordingly
                lt_failure_mode.inspection_costs = lt_failure_mode.corrective_maintenance_costs / inspection_monitoring_ratio
                lt_failure_mode.sensor_costs = lt_failure_mode.corrective_maintenance_costs / equipment_monitoring_ratio

                #Simular a política de manutenção pretendida e guardar o melhor resultado
                decision, cost, lifetimes = scaled_maintenance_policy_optimal_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)

                #save the obtained results
                optimal_decision.append(decision), optimal_cost.append(cost), optimal_lifetime.append(lifetimes)

                #always reset the costs to the original value at the end of the analysis
                lt_failure_mode.preventive_maintenance_costs, lt_failure_mode.corrective_maintenance_costs = lt_preventive_maintenance_costs, lt_corrective_maintenance_costs
                st_failure_mode.preventive_maintenance_costs, st_failure_mode.corrective_maintenance_costs = st_preventive_maintenance_costs, st_corrective_maintenance_costs
                lt_failure_mode.sensor_costs, lt_failure_mode.inspection_costs = original_monitoring_equipment_cost, original_inspection_cost

            #return the results in a pandas dataframe
            agregated_results[f"optimal_decision_{maintenance_policy}"] = optimal_decision
            agregated_results[f"optimal_cost_{maintenance_policy}"] = optimal_cost
            agregated_results[f"optimal_lifetime_{maintenance_policy}"] = optimal_lifetime

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
#ratio_limit - Defines the ratio maximum value that is going to be used for the study
#sensitivity_step - The iterative step that we want when going through the interval
def failure_modes_shocks_intensity(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, ratio_limit, sensitivity_step):

    #define the mtbf ratio that we want to study
    ratio_interval = [ratio for ratio in range(1,ratio_limit,sensitivity_step)]
    ratio_interval.append(ratio_limit) #garantuee that we add the maximum allowed value for the ratio

    #Compute the average degradation given the long-term failure mode MTBF and the failure threshold
    average_delta = lt_failure_mode.compute_mtbf('wienner')/lt_failure_mode.failure_threshold

    #Dataframe to save the results
    agregated_results = pd.DataFrame({"shock_intensity_ratio": ratio_interval})

    #analyze the process for each maintenance policy that we have available
    for maintenance_policy in maintenance_policy_list:
        #define the variabless that will save the results of interest
        optimal_decision, optimal_cost, optimal_lifetime = list(), list(), list()

        #analyse a given ratio value
        for ratio in ratio_interval:

            #output progress
            print(f'{maintenance_policy} - The ratio value between the degradation with shocks and the average degradation is R={ratio}')

            #Calcular o drift que precisamos dado o rácio e mantendo o resto da informação (temos que ajustar o ratio para a escala real)
            new_shock_intensity_mean = ratio * average_delta - average_delta

            #Simular a política de manutenção pretendida e guardar o melhor resultado
            decision, cost, lifetimes = scaled_maintenance_policy_optimal_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, new_shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)

            #save the obtained results
            optimal_decision.append(decision), optimal_cost.append(cost), optimal_lifetime.append(lifetimes)

        #return the results in a pandas dataframe
        agregated_results[f"optimal_decision_{maintenance_policy}"] = optimal_decision
        agregated_results[f"optimal_cost_{maintenance_policy}"] = optimal_cost
        agregated_results[f"optimal_lifetime_{maintenance_policy}"] = optimal_lifetime

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
#ratio_limit - Defines the ratio maximum value that is going to be used for the study
#sensitivity_step - The iterative step that we want when going through the interval
def failure_modes_condition_costs(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, ratio_limit, sensitivity_step):

    #define the mtbf ratio that we want to study
    ratio_interval = [ratio for ratio in range(1,ratio_limit,sensitivity_step)]
    ratio_interval.append(ratio_limit) #garantuee that we add the maximum allowed value for the ratio

    #Dataframe to save the results
    agregated_results = pd.DataFrame({"condition_costs_ratio": ratio_interval})

    #original costs (we assume that is installed for the long-term failure!)
    original_monitoring_equipment_cost, original_inspection_cost = lt_failure_mode.sensor_costs, lt_failure_mode.inspection_costs
    st_corrective_maintenance_costs, st_preventive_maintenance_costs = st_failure_mode.corrective_maintenance_costs, st_failure_mode.preventive_maintenance_costs
    lt_corrective_maintenance_costs, lt_preventive_maintenance_costs = lt_failure_mode.corrective_maintenance_costs, lt_failure_mode.preventive_maintenance_costs

    #compute the original ratio
    lt_corrective_maintenance_monitoring_ratio, st_corrective_maintenance_monitoring_ratio = lt_failure_mode.corrective_maintenance_costs / original_monitoring_equipment_cost, st_failure_mode.corrective_maintenance_costs / original_monitoring_equipment_cost
    lt_preventive_maintenance_monitoring_ratio, st_preventive_maintenance_monitoring_ratio = lt_failure_mode.preventive_maintenance_costs / original_monitoring_equipment_cost, st_failure_mode.preventive_maintenance_costs / original_monitoring_equipment_cost

    #analyze the process for each maintenance policy that we have available
    for maintenance_policy in maintenance_policy_list:
        #define the variabless that will save the results of interest
        optimal_decision, optimal_cost, optimal_lifetime = list(), list(), list()

        #analyse a given ratio value
        for ratio in ratio_interval:

            #output progress
            print(f'{maintenance_policy} - The ratio value between the sensor cost and the inspection cost is R={ratio}')

            #Calcular o custo do sensor com base no custo de inspeção definido (we assume that is installed for the long-term failure!)
            lt_failure_mode.sensor_costs = ratio * lt_failure_mode.inspection_costs

            #Adjust the maintenance costs in order to isolate the effect of the monitoring costs
            #st_failure_mode.corrective_maintenance_costs, st_failure_mode.preventive_maintenance_costs = lt_failure_mode.sensor_costs * st_corrective_maintenance_monitoring_ratio, lt_failure_mode.sensor_costs * st_preventive_maintenance_monitoring_ratio
            #lt_failure_mode.corrective_maintenance_costs, lt_failure_mode.preventive_maintenance_costs = lt_failure_mode.sensor_costs * lt_corrective_maintenance_monitoring_ratio, lt_failure_mode.sensor_costs * lt_preventive_maintenance_monitoring_ratio

            #Simular a política de manutenção pretendida e guardar o melhor resultado
            if check_sensitivity_influence(maintenance_policy, ['TBM', 'ICBM'], optimal_decision) == True:
                decision, cost, lifetimes = scaled_maintenance_policy_optimal_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)

            #save the obtained results
            optimal_decision.append(decision), optimal_cost.append(cost), optimal_lifetime.append(lifetimes)

            #always reset the costs to the original value at the end of the analysis
            lt_failure_mode.preventive_maintenance_costs, lt_failure_mode.corrective_maintenance_costs = lt_preventive_maintenance_costs, lt_corrective_maintenance_costs
            st_failure_mode.preventive_maintenance_costs, st_failure_mode.corrective_maintenance_costs = st_preventive_maintenance_costs, st_corrective_maintenance_costs
            lt_failure_mode.sensor_costs, lt_failure_mode.inspection_costs = original_monitoring_equipment_cost, original_inspection_cost

        #return the results in a pandas dataframe
        agregated_results[f"optimal_decision_{maintenance_policy}"] = optimal_decision
        agregated_results[f"optimal_cost_{maintenance_policy}"] = optimal_cost
        agregated_results[f"optimal_lifetime_{maintenance_policy}"] = optimal_lifetime

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
#ratio_limit - Defines the ratio maximum value that is going to be used for the study
#sensitivity_step - The iterative step that we want when going through the interval
def maintenance_to_condition_costs(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, ratio_limit, sensitivity_step):

    #define the mtbf ratio that we want to study
    ratio_interval = [ratio for ratio in range(1,ratio_limit,sensitivity_step)]
    ratio_interval.append(ratio_limit) #garantuee that we add the maximum allowed value for the ratio

    #Dataframe to save the results
    agregated_results = pd.DataFrame({"condition_costs_ratio": ratio_interval})

    #original costs (we assume that is installed for the long-term failure!)
    original_monitoring_equipment_cost, original_inspection_cost = lt_failure_mode.sensor_costs, lt_failure_mode.inspection_costs
    st_corrective_maintenance_costs, st_preventive_maintenance_costs = st_failure_mode.corrective_maintenance_costs, st_failure_mode.preventive_maintenance_costs
    lt_corrective_maintenance_costs, lt_preventive_maintenance_costs = lt_failure_mode.corrective_maintenance_costs, lt_failure_mode.preventive_maintenance_costs

    #compute the original ratio
    #lt_corrective_maintenance_monitoring_ratio, st_corrective_maintenance_monitoring_ratio = lt_failure_mode.corrective_maintenance_costs / original_monitoring_equipment_cost, st_failure_mode.corrective_maintenance_costs / original_monitoring_equipment_cost
    #lt_preventive_maintenance_monitoring_ratio, st_preventive_maintenance_monitoring_ratio = lt_failure_mode.preventive_maintenance_costs / original_monitoring_equipment_cost, st_failure_mode.preventive_maintenance_costs / original_monitoring_equipment_cost
    #inspection_monitoring_ratio = original_monitoring_equipment_cost / lt_failure_mode.inspection_costs

    #analyze the process for each maintenance policy that we have available
    for maintenance_policy in maintenance_policy_list:
        #analyse the costs given its type (corrective or preventive)
        for costs_type in ['preventive','corrective']:
            #define the variabless that will save the results of interest
            optimal_decision, optimal_cost, optimal_lifetime = list(), list(), list()
            #analyse a given ratio value
            for ratio in agregated_results.iloc[:, 0]:

                #output progress
                print(f'{maintenance_policy} - The costs ratio value between the short-term and long-term failure is R={ratio}')

                #compute the new costs threshold based on the specified ratio
                if costs_type == 'preventive':
                    lt_failure_mode.sensor_costs = lt_failure_mode.preventive_maintenance_costs / ratio #influences the CBM policy
                    lt_failure_mode.inspection_costs = lt_failure_mode.preventive_maintenance_costs / ratio #influences the ICBM policy
                    #lt_failure_mode.corrective_maintenance_costs = lt_failure_mode.sensor_costs * lt_corrective_maintenance_monitoring_ratio
                else:
                    lt_failure_mode.sensor_costs = lt_failure_mode.corrective_maintenance_costs / ratio #influences the CBM policy
                    lt_failure_mode.inspection_costs = lt_failure_mode.corrective_maintenance_costs / ratio #influences the ICBM policy
                    #lt_failure_mode.preventive_maintenance_costs = lt_failure_mode.sensor_costs * lt_preventive_maintenance_monitoring_ratio

                #Adjust the inspection costs and short_term failure mode maintenance costs accordingly
                #lt_failure_mode.inspection_costs = lt_failure_mode.sensor_costs / inspection_monitoring_ratio
                #st_failure_mode.corrective_maintenance_costs, st_failure_mode.preventive_maintenance_costs = lt_failure_mode.sensor_costs * st_corrective_maintenance_monitoring_ratio, lt_failure_mode.sensor_costs * st_preventive_maintenance_monitoring_ratio

                #Simular a política de manutenção pretendida e guardar o melhor resultado
                if check_sensitivity_influence(maintenance_policy, ['TBM'], optimal_decision) == True:
                    decision, cost, lifetimes = scaled_maintenance_policy_optimal_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)

                #save the obtained results
                optimal_decision.append(decision), optimal_cost.append(cost), optimal_lifetime.append(lifetimes)

                #always reset the costs to the original value at the end of the analysis
                lt_failure_mode.preventive_maintenance_costs, lt_failure_mode.corrective_maintenance_costs = lt_preventive_maintenance_costs, lt_corrective_maintenance_costs
                st_failure_mode.preventive_maintenance_costs, st_failure_mode.corrective_maintenance_costs = st_preventive_maintenance_costs, st_corrective_maintenance_costs
                lt_failure_mode.sensor_costs, lt_failure_mode.inspection_costs = original_monitoring_equipment_cost, original_inspection_cost

            #return the results in a pandas dataframe
            agregated_results[f"optimal_decision_{maintenance_policy}"] = optimal_decision
            agregated_results[f"optimal_cost_{maintenance_policy}"] = optimal_cost
            agregated_results[f"optimal_lifetime_{maintenance_policy}"] = optimal_lifetime

    #final table
    return agregated_results

#Study the influence of the error variability
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
#ratio_limit - Defines the ratio maximum value that is going to be used for the study
#sensitivity_step - The iterative step that we want when going through the interval
def failure_modes_monitoring_error(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy_list, policy_limit, policy_step, ratio_limit, sensitivity_step):

    #define the shock ratio between the time between shocks and the short-term failure mode mtbf
    ratio_interval = [ratio for ratio in range(1,ratio_limit,sensitivity_step)]
    ratio_interval.append(ratio_limit) #garantue that we add the maximum allowed value for the ratio

    #Dataframe to save the results
    agregated_results = pd.DataFrame({"error_variability": ratio_interval})

    #scale the ratio values according to the error (we want the error in percentage)
    agregated_results['error_variability'] = agregated_results['error_variability']/100

    #analyze the process for each maintenance policy that we have available
    for maintenance_policy in maintenance_policy_list:
        #define the variabless that will save the results of interest
        optimal_decision, optimal_cost, optimal_lifetime = list(), list(), list()

        #analyse a given ratio value
        for ratio in agregated_results.iloc[:, 0]:

            #output progress
            print(f'{maintenance_policy} - The error value variability is sigma={ratio}')

            #compute the new shock threshold based on the specified ratio
            lt_failure_mode.uncertainty_level, st_failure_mode.uncertainty_level = ratio, ratio

            #Simular a política de manutenção pretendida e guardar o melhor resultado
            if check_sensitivity_influence(maintenance_policy, ['TBM','CBM','ICBM'], optimal_decision) == True:
                decision, cost, lifetimes = scaled_maintenance_policy_optimal_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)

            #save the obtained results
            optimal_decision.append(decision), optimal_cost.append(cost), optimal_lifetime.append(lifetimes)

        #return the results in a pandas dataframe
        agregated_results[f"optimal_decision_{maintenance_policy}"] = optimal_decision
        agregated_results[f"optimal_cost_{maintenance_policy}"] = optimal_cost
        agregated_results[f"optimal_lifetime_{maintenance_policy}"] = optimal_lifetime

    #final table
    return agregated_results

#Verify if we neeed to compute a new value for the maintenance policy given the parameters variation
def check_sensitivity_influence(maintenance_policy, check_maintenance_policy_list, optimal_decision_list):

    return False if (maintenance_policy in check_maintenance_policy_list) and (len(optimal_decision_list) > 0) else True

#Scale the values according to the best and worst possible result
#Parameters:
#lt_failure_mode - Long term failure mode object that is used for the degradation process
#st_failure_mode - Short term failure mode object that is used for the degradation process
#shock_threshold - Shock threshold
#shock_lameda - Poisson arrival rate for the shock process
#shock_mean - Normal distribution mean parameter
#shock_stdev - Normal distribution standard deviation parameter
#number_periods - Number of time periods that are used for the simulation
#maintenance_policy_list - Compute the costs according to the defined maintenance policy list (CM - corrective maintenance, PM - perfect maintenance, TBM - time based maintenance, ICBM - with perfect inspection, CBM - with perfect continuous monitoring, EICBM - with imperfect inspection, ECBM - with imperfect continuous monitoring)
#policy_limit - Limit to where we can iteratively study the respective maintenance policy
#policy_step - Number of times that we want to make a step (by default it takes the unit value)
#inspection_policy_step - The iterative step that we want when going through the interval of the inspection based maintenance
def scaled_maintenance_policy_optimal_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step, inspection_policy_step = 5):

    #Worst possible result
    _, worst_cost, _, _ = optimal_maintenance_policy_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, 'CM', policy_limit, policy_step)

    #Scale results according to the maintenance policy
    if maintenance_policy== 'ICBM':
        cost = 99999 #really high value
        for inspection_time in range(1,int(lt_failure_mode.compute_mtbf('gamma')),inspection_policy_step):
            st_failure_mode.inspection, lt_failure_mode.inspection = inspection_time, inspection_time #test different inspection times for the inspection based condition based maintenance
            #simulate the process
            computed_optimal_decision, computed_cost, computed_optimal_lifetimes, _ = optimal_maintenance_policy_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)
            #check if we update the results
            if computed_cost < cost:
                cost = computed_cost #new best cost
                optimal_decision = computed_optimal_decision #new best decision
                optimal_lifetimes = computed_optimal_lifetimes #new best lifetime
    #in case we use another maintenance policy
    else:
        optimal_decision, cost, optimal_lifetimes, _ = optimal_maintenance_policy_cost(lt_failure_mode, st_failure_mode, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, maintenance_policy, policy_limit, policy_step)

    return optimal_decision, round(cost/worst_cost,2), optimal_lifetimes

#Plot the results according to the paper format
#Parameters:
#sensitivity_results - Provide the pandas dataframe with the results
#x_axis_name - X axis label name
#y_axis_name - Y axis label name
def plot_sensitivity_analysis_results(sensitivity_results, x_axis_name, y_axis_name):

    ##build inspection policy
    fig, ax = plt.subplots(figsize=(20, 10))

    #get feature of interest to study (alterar esta parte para mais geral!!!!!)
    columns_of_interest = [col for col in sensitivity_results.iloc[:, 1:].columns if 'optimal_cost' in col]

    #plot the results for the required maintenance policies
    for col in columns_of_interest:
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

