####################################################
###Funções dedicadas à degradação dos ativos     ###
####################################################

#Generic libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
#lt_failure_mode - Long term failure mode object that is used for the degradation process
#st_failure_mode - Short term failure mode object that is used for the degradation process
#maintenance_policy - Compute the costs according to the defined maintenance policy (CM - corrective maintenance,TBM - time based maintenance, ICBM - with perfect inspection, CBM - with perfect continuous monitoring, EICBM - with imperfect inspection, ECBM - with imperfect continuous monitoring)
def maintenance_costs(lt_failure_mode, st_failure_mode, maintenance_policy):

    #Get the maintenance interventions
    st_maintenance = maintenance_interventions(st_failure_mode.degradation, st_failure_mode.initial_condition, st_failure_mode.failure_threshold)
    lt_maintenance = maintenance_interventions(lt_failure_mode.degradation, lt_failure_mode.initial_condition, lt_failure_mode.failure_threshold)

    #Compute costs for the corrective maintenance costs
    if maintenance_policy == 'CM':
        total_corrective_maintenance_costs = st_maintenance.count('C') * st_failure_mode.corrective_maintenance_costs + lt_maintenance.count('C') * lt_failure_mode.corrective_maintenance_costs

    return total_corrective_maintenance_costs

#Function to compute the expected lifetime of a failure mode given the simulated degradation
def expected_lifetime(failure_mode_degradation, initial_condition):

    return np.mean(np.diff(get_restart_condition_time(failure_mode_degradation, initial_condition)))

#Function to record the failure time for a given simulated degradation
def get_restart_condition_time(failure_mode_degradation, initial_condition):

    return [time for time in range(len(failure_mode_degradation)) if failure_mode_degradation[time] == initial_condition]
