####################################################
###Funções dedicadas à degradação dos ativos     ###
####################################################

#Generic libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Failure mode degradation that leads to the asset failure and consequent replacement
#Parameters:
#failure_mode_condition - Failure mode condition before the degradation
#scale - Gamma distribution scale parameter
#shape - Gamma distribution shape parameter
def long_term_failure_mode_degradation(failure_mode_condition, scale, shape):

    return failure_mode_condition + np.random.gamma(shape, scale)

#Failure mode degradation that leads to the asset repair but not replacement
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
def simulate_degradation(lt_initial_condition, lt_failure_threshold, lt_scale, lt_shape,
                         st_initial_condition, st_failure_threshold, st_mean, st_stdev, shock_threshold,
                         shock_lameda, shock_mean, shock_stdev, number_periods):

    #Variables that keep the degradation results
    lt_results = list()
    st_results = list()

    #Variables that are meant for the condition
    lt_condition = lt_initial_condition
    st_condition = st_initial_condition

    #Simulate degradation of failure mode 1
    for i in range(number_periods):

        #Save the results
        st_results.append(st_condition), lt_results.append(lt_condition)

        #simulate the period degradation
        st_condition = short_term_failure_mode_degradation(st_condition, st_mean, st_stdev)
        lt_condition = long_term_failure_mode_degradation(lt_condition, lt_scale, lt_shape)

        #Check the shock period
        lt_condition = shock_simulation(lt_condition, shock_lameda, shock_mean, shock_stdev) if st_condition > shock_threshold else lt_condition

        #Check failure occurrence
        lt_condition = lt_initial_condition if lt_condition > lt_failure_threshold else lt_condition
        st_condition = st_initial_condition if st_condition > st_failure_threshold else st_condition


    return st_results, lt_results

#Function to plot the degradation process
#Parameters:
def degradation_plot(st_degradation,lt_degradation):

    #build degradation plot
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(np.array(range(len(st_degradation))), np.array(st_degradation))
    ax.plot(np.array(range(len(lt_degradation))), np.array(lt_degradation))

    #Plot labeling
    ax.set(xlabel='Time (days)', ylabel='Degradation', title='Degradation sample')

    #Show results
    plt.show()

#Results example
short_term,long_term = simulate_degradation(0, 200, 0.1, 2,
                           10, 100, 2, 4, 50,
                           0.5, 7, 2, 1000)

degradation_plot(short_term,long_term)