####################################################
###Funções dedicadas à degradação dos ativos     ###
####################################################

#Generic libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from failure_mode_class import Failure_mode_degradation

#Failure mode degradation that leads to the asset failure and consequent replacement using a gamma process
#Parameters:
#failure_mode_condition - Failure mode condition before the degradation
#scale - Gamma distribution scale parameter
#shape - Gamma distribution shape parameter
def long_term_failure_mode_degradation(failure_mode_condition, scale, shape):

    return failure_mode_condition + np.random.gamma(shape, scale)

#Failure mode degradation that leads to the asset repair but not replacement using a wienner process
#Parameters:
#failure_mode_condition - Failure mode condition before the degradation
#mean - Normal distribution mean parameter
#stdev - Normal distribution standard deviation parameter
def short_term_failure_mode_degradation(failure_mode_condition, mean, stdev):

    return failure_mode_condition + np.random.normal(mean, stdev)

#Shock process simulation
#Parameters:
#failure_mode_condition - Failure mode condition before the degradation
#lameda - Shock arrival rate
#mean - Normal distribution mean parameter
#stdev - Normal distribution standard deviation parameter
def shock_simulation(failure_mode_condition, lameda, mean, stdev):

    return failure_mode_condition + np.random.normal(mean, stdev) if np.random.poisson(lameda) > 0 else failure_mode_condition

#Degradation simulator without maintenance (corrective maintenance)
#Parameters:
#lt_failure_mode - Long term failure mode object that is used for the degradation process
#st_failure_mode - Short term failure mode object that is used for the degradation process
#shock_threshold - Shock threshold
#shock_lameda - Poisson arrival rate for the shock process
#shock_mean - Normal distribution mean parameter
#shock_stdev - Normal distribution standard deviation parameter
#number_periods - Number of time periods that are used for the simulation
def simulate_degradation(lt_failure_mode, st_failure_mode, shock_threshold, shock_lameda, shock_mean, shock_stdev, number_periods):

    #Auxiliary variables that are meant for the condition
    st_condition, lt_condition = st_failure_mode.initial_condition, lt_failure_mode.initial_condition

    #Simulate degradation of failure mode 1
    for i in range(number_periods):

        #Save the results
        st_failure_mode.degradation.append(st_condition), lt_failure_mode.degradation.append(lt_condition)

        #Check failure occurrence
        st_condition = st_failure_mode.initial_condition if ((st_condition > st_failure_mode.failure_threshold) or (lt_condition > lt_failure_mode.failure_threshold)) else st_condition
        lt_condition = lt_failure_mode.initial_condition if lt_condition > lt_failure_mode.failure_threshold else lt_condition

        #Save again the results if there was a reset in the condition
        if (st_condition == st_failure_mode.initial_condition) or (lt_condition == lt_failure_mode.initial_condition):
            st_failure_mode.degradation.append(st_condition), lt_failure_mode.degradation.append(lt_condition)

        #simulate the period degradation
        st_condition = short_term_failure_mode_degradation(st_condition, st_failure_mode.average_degradation_parameter, st_failure_mode.variability_degradation_parameter)
        lt_condition = long_term_failure_mode_degradation(lt_condition, lt_failure_mode.average_degradation_parameter, lt_failure_mode.variability_degradation_parameter)

        #Check the shock period
        lt_condition = shock_simulation(lt_condition, shock_lameda, shock_mean, shock_stdev) if st_condition > shock_threshold else lt_condition

    #delete the first recorded values since it contains a duplicate recording
    del st_failure_mode.degradation[0]
    del lt_failure_mode.degradation[0]

    return st_failure_mode, lt_failure_mode

#Degradation simulator with maintenance (corrective maintenance)
#Parameters:
#lt_failure_mode - Long term failure mode object that is used for the degradation process
#st_failure_mode - Short term failure mode object that is used for the degradation process
#shock_threshold - Shock threshold
#shock_lameda - Poisson arrival rate for the shock process
#shock_mean - Normal distribution mean parameter
#shock_stdev - Normal distribution standard deviation parameter
#number_periods - Number of time periods that are used for the simulation
#maintenance_policy - Compute the costs according to the defined maintenance policy (CM - corrective maintenance, TBM - time based maintenance, ICBM - with perfect inspection, CBM - with perfect continuous monitoring, EICBM - with imperfect inspection, ECBM - with imperfect continuous monitoring)
def simulate_degradation_with_maintenance(lt_failure_mode, st_failure_mode, shock_threshold, shock_lameda, shock_mean, shock_stdev, number_periods, maintenance_policy):

    #Auxiliary variables that are meant for the condition
    st_condition, lt_condition = st_failure_mode.initial_condition, lt_failure_mode.initial_condition

    #Simulate degradation of failure mode 1
    for i in range(number_periods):

        #Save the results
        st_failure_mode.degradation.append(st_condition), lt_failure_mode.degradation.append(lt_condition)

        #Check failure occurrence
        st_condition = st_failure_mode.initial_condition if ((st_condition > st_failure_mode.failure_threshold) or (lt_condition > lt_failure_mode.failure_threshold)) else st_condition
        lt_condition = lt_failure_mode.initial_condition if lt_condition > lt_failure_mode.failure_threshold else lt_condition

        #Check condition based maintenance policy
        if maintenance_policy == 'CBM':
            st_condition = st_failure_mode.initial_condition if ((st_condition > st_failure_mode.condition_maintenance_threshold) or (lt_condition > lt_failure_mode.condition_maintenance_threshold)) else st_condition
            lt_condition = lt_failure_mode.initial_condition if lt_condition > lt_failure_mode.condition_maintenance_threshold else lt_condition

        #Save again the results if there was a reset in the condition
        if (st_condition == st_failure_mode.initial_condition) or (lt_condition == lt_failure_mode.initial_condition):
            st_failure_mode.degradation.append(st_condition), lt_failure_mode.degradation.append(lt_condition)

        #simulate the period degradation
        st_condition = short_term_failure_mode_degradation(st_condition, st_failure_mode.average_degradation_parameter, st_failure_mode.variability_degradation_parameter)
        lt_condition = long_term_failure_mode_degradation(lt_condition, lt_failure_mode.average_degradation_parameter, lt_failure_mode.variability_degradation_parameter)

        #Check the shock period
        lt_condition = shock_simulation(lt_condition, shock_lameda, shock_mean, shock_stdev) if st_condition > shock_threshold else lt_condition

    #delete the first recorded values since it contains a duplicate recording
    del st_failure_mode.degradation[0]
    del lt_failure_mode.degradation[0]

    return st_failure_mode, lt_failure_mode

#Function to plot the degradation process
#Parameters:
#st_degradation - Short therm failure mode simulated degradation
#st_failure_threshold - Short therm failure mode failure threshold
#shock_threshold - Shock threshold
#lt_degradation - Long therm failure mode simulated degradation
#lt_failure_threshold - Long therm failure mode failure threshold
def degradation_plot(st_degradation, st_failure_threshold, shock_threshold, lt_degradation, lt_failure_threshold):

    #build degradation plot
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(np.array(range(len(st_degradation))), np.array(st_degradation), label="short term failure mode")
    ax.plot(np.array(range(len(lt_degradation))), np.array(lt_degradation), label="long term failure mode")

    #add failure thresholds
    ax.plot(np.array(range(len(st_degradation))), [st_failure_threshold] * len(st_degradation), label="short term failure threshold")
    ax.plot(np.array(range(len(st_degradation))), [shock_threshold] * len(st_degradation), label="shock threshold")
    ax.plot(np.array(range(len(lt_degradation))), [lt_failure_threshold] * len(lt_degradation), label="long term failure threshold")

    #Plot labeling
    ax.set(xlabel='Time (days)', ylabel='Degradation', title='Degradation sample')

    #Show results
    plt.legend(loc='upper left')
    plt.show()

#Function to plot the expected unitary cost process
#Parameters:
#st_expected_unitary_cost - Expected unitary costs vector for the short-term failure mode
#lt_expected_unitary_cost - Expected unitary costs vector for the long-term failure mode
#policy_iteration_limit - Limit to where we can iteratively study the respective maintenance policy
#policy_step - Number of times that we want to make a step (by default it takes the unit value)
#decision - decision variable for the maintenance policy
#y_axis_limit - specify plot y axis upper limit
def policy_costs_plot(st_expected_unitary_cost, lt_expected_unitary_cost, policy_iteration_limit, policy_step, decision, y_axis_limit):

    #build degradation plot
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(np.array(range(int(policy_iteration_limit/policy_step)))*policy_step, np.array(st_expected_unitary_cost), label="short term failure mode")
    ax.plot(np.array(range(int(policy_iteration_limit/policy_step)))*policy_step, np.array(lt_expected_unitary_cost), label="long term failure mode")

    #add thresholds
    ax.plot([st_expected_unitary_cost.index(min(st_expected_unitary_cost))*policy_step] * len(st_expected_unitary_cost), np.array(st_expected_unitary_cost), label="short term best threshold")
    ax.plot([lt_expected_unitary_cost.index(min(lt_expected_unitary_cost))*policy_step] * len(lt_expected_unitary_cost), np.array(lt_expected_unitary_cost), label="long term best threshold")

    #Plot labeling
    ax.set(xlabel=decision, ylabel='Expected unitary cost')

    #Plot ylim
    plt.ylim(0,y_axis_limit)

    #Show results
    plt.legend(loc='upper left')
    plt.show()

#Function to assess if there was a corrective or a preventive replacement according to the degradation
#Parameters:
#condition_degradation - Array with the failure mode simulated degradation over N periods
#initial_condition - Short-term failure mode initial degradation
#failure_threshold - Short-term failure mode failure threshold
def maintenance_interventions(condition_degradation, initial_condition, failure_threshold):

    return [classify_maintenance_intervetion(condition_degradation[i],failure_threshold) for i in range(len(condition_degradation)-1) if condition_degradation[i+1] == initial_condition]

#Function to classify if an intervention was preventive or corrective whenever there is a condition reset
#Parameters:
#degradation - Period degradation
#failure_threshold - Short-term failure mode failure threshold
def classify_maintenance_intervetion(degradation, failure_threshold):

    return 'C' if degradation > failure_threshold else 'P'

#Function to compute costs the maintenance costs
#Parameters:
#failure_mode - Failure mode object that is used for the degradation process
#maintenance_policy - Compute the costs according to the defined maintenance policy (CM - corrective maintenance,TBM - time based maintenance, ICBM - with perfect inspection, CBM - with perfect continuous monitoring, EICBM - with imperfect inspection, ECBM - with imperfect continuous monitoring)
def maintenance_costs(failure_mode, maintenance_policy):

    #Get the maintenance interventions
    failure_mode_maintenance = maintenance_interventions(failure_mode.degradation, failure_mode.initial_condition, failure_mode.failure_threshold)

    #Compute costs for the corrective maintenance costs
    #if maintenance_policy == 'CM':
    total_maintenance_costs = (failure_mode_maintenance.count('C') * failure_mode.corrective_maintenance_costs) / len(failure_mode_maintenance) + \
                              (failure_mode_maintenance.count('P') * failure_mode.preventive_maintenance_costs) / len(failure_mode_maintenance)

    return round(total_maintenance_costs, 2)

#Function to compute the expected lifetime of a failure mode given the simulated degradation
#Parameters:
#failure_mode_degradation - List containing the degradation of a particular failure mode
#initial_condition - Failure mode initial condition
def expected_lifetime(failure_mode_degradation, initial_condition):

    return np.mean(np.diff(get_restart_condition_time(failure_mode_degradation, initial_condition)))

#Function to record the failure time for a given simulated degradation
#Parameters:
#failure_mode_degradation - List containing the degradation of a particular failure mode
#initial_condition - Failure mode initial condition
def get_restart_condition_time(failure_mode_degradation, initial_condition):

    return [time for time in range(len(failure_mode_degradation)) if failure_mode_degradation[time] == initial_condition]

#Function to compute the reliability function
def compute_reliability_function(failure_mode, number_periods, step):

    #Get the failure times
    failure_times = list(np.diff(get_restart_condition_time(failure_mode.degradation, failure_mode.initial_condition)))

    #Compute the reliability function
    return [len(list(filter(lambda number: number >= i * step, failure_times)))/len(failure_times) for i in range(int(number_periods / step))]


#Function to simulate a given maintenance policy
#lt_failure_mode - Long term failure mode object that is used for the degradation process
#st_failure_mode - Short term failure mode object that is used for the degradation process
#shock_threshold - Shock threshold
#shock_lameda - Poisson arrival rate for the shock process
#shock_mean - Normal distribution mean parameter
#shock_stdev - Normal distribution standard deviation parameter
#number_periods - Number of time periods that are used for the simulation
#maintenance_policy - Compute the costs according to the defined maintenance policy (CM - corrective maintenance,TBM - time based maintenance, ICBM - with perfect inspection, CBM - with perfect continuous monitoring, EICBM - with imperfect inspection, ECBM - with imperfect continuous monitoring)
#policy_iteration_limit - Limit to where we can iteratively study the respective maintenance policy
#policy_step - Number of times that we want to make a step (by default it takes the unit value)
def simulate_maintenance_policy(lt_failure_mode, st_failure_mode, shock_threshold, shock_lameda, shock_mean, shock_stdev, number_periods, maintenance_policy, policy_iteration_limit, policy_step=1):

    #variable that will keep the results
    st_expected_maintenance_cost_per_unit_of_time = list()
    lt_expected_maintenance_cost_per_unit_of_time = list()
    results_index = list()

    #Compute costs for the corrective maintenance costs
    if maintenance_policy == 'CM':

        #simulate the degradation of both failure modes given the corrective maintenance
        st_failure_mode, lt_failure_mode = simulate_degradation(lt_failure_mode, st_failure_mode, shock_threshold, shock_lameda, shock_mean, shock_stdev, number_periods)

        #Compute the expected unitary cost for each failure mode
        st_expected_maintenance_cost_per_unit_of_time.append(maintenance_costs(st_failure_mode, maintenance_policy) / expected_lifetime(st_failure_mode.degradation, st_failure_mode.initial_condition))
        lt_expected_maintenance_cost_per_unit_of_time.append(maintenance_costs(lt_failure_mode, maintenance_policy) / expected_lifetime(lt_failure_mode.degradation, lt_failure_mode.initial_condition))

    #Compute cost for the time based maintenance
    if maintenance_policy == 'TBM':

        #simulate the degradation of both failure modes given the conndition based maintenance
        st_failure_mode, lt_failure_mode = simulate_degradation(lt_failure_mode, st_failure_mode, shock_threshold, shock_lameda, shock_mean, shock_stdev, number_periods)

        #Compute the reliability function for each failure mode
        st_reliability_function, lt_reliability_function = compute_reliability_function(st_failure_mode, policy_iteration_limit, policy_step), compute_reliability_function(lt_failure_mode, policy_iteration_limit, policy_step)

        #Compute the expected lifetime for each failure mode (do not forget to multiply by the policy step since it represents the integral rectangle width)
        st_expected_lifetime_tbm, lt_expected_lifetime_tbm = list(np.cumsum(st_reliability_function)*policy_step), list(np.cumsum(lt_reliability_function)*policy_step)

        #Compute the expected unitary cost per failure mode according to the renewal theory
        st_expected_maintenance_cost_per_unit_of_time = [(1-reliability)*st_failure_mode.corrective_maintenance_costs/expected_lifetime + reliability*st_failure_mode.preventive_maintenance_costs/expected_lifetime for reliability,expected_lifetime in zip(st_reliability_function, st_expected_lifetime_tbm)]
        lt_expected_maintenance_cost_per_unit_of_time = [(1-reliability)*lt_failure_mode.corrective_maintenance_costs/expected_lifetime + reliability*lt_failure_mode.preventive_maintenance_costs/expected_lifetime for reliability,expected_lifetime in zip(lt_reliability_function, lt_expected_lifetime_tbm)]

    #Compute cost for the continuous based maintenance with perfect inspection
    if maintenance_policy == 'CBM':

        #Simulate for different combinations of condition thresholds
        for lt_cbm in range(1, lt_failure_mode.failure_threshold+1, policy_step):
            for st_cbm in range(1, st_failure_mode.failure_threshold+1, policy_step):

                #simulate the degradation of both failure modes according to the condition based thresholds
                st_failure_mode.condition_maintenance_threshold, lt_failure_mode.condition_maintenance_threshold = st_cbm, lt_cbm
                st_failure_mode, lt_failure_mode = simulate_degradation_with_maintenance(lt_failure_mode, st_failure_mode, shock_threshold, shock_lameda, shock_mean, shock_stdev, number_periods, maintenance_policy)

                #Compute the expected unitary cost for each failure mode
                results_index.append(f'{lt_cbm}/{st_cbm}')
                st_expected_maintenance_cost_per_unit_of_time.append(maintenance_costs(st_failure_mode, maintenance_policy) / expected_lifetime(st_failure_mode.degradation, st_failure_mode.initial_condition))
                lt_expected_maintenance_cost_per_unit_of_time.append(maintenance_costs(lt_failure_mode, maintenance_policy) / expected_lifetime(lt_failure_mode.degradation, lt_failure_mode.initial_condition))


    #Return the expected unitary cost for the studied failure modes
    return results_index, st_expected_maintenance_cost_per_unit_of_time, lt_expected_maintenance_cost_per_unit_of_time

#Test functions
short_term = Failure_mode_degradation(10, 100, 2, 4, [], 100, 50, 200)
long_term = Failure_mode_degradation(0, 200, 0.1, 2, [], 200, 200, 1000)
shock_threshold = 50
lameda_shocks = 0.5 #shocks per time step
shock_intensity_mean = 7 #normal distribution
shock_intensity_stdev = 2 #normal distribution
simulating_periods = 1000

results_index, st_expected_maintenance_cost_per_unit_of_time, lt_expected_maintenance_cost_per_unit_of_time = simulate_maintenance_policy(long_term, short_term, shock_threshold, lameda_shocks, shock_intensity_mean, shock_intensity_stdev, simulating_periods, 'CBM', 200, 5)

#policy_costs_plot(st_expected_maintenance_cost_per_unit_of_time, lt_expected_maintenance_cost_per_unit_of_time, 200, 1, "Time (t)", 50)