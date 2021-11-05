####################################################
###Class to model the failure degradation        ###
####################################################

class Failure_mode_degradation:

    #Initialize object
    #Parameters:
    #initial_condition - Failure mode initial condition
    #failure_threshold - Failure mode failure threshold
    #average_degradation_parameter - statistical distribution parameter that is linked to the mean (ex: for the normal distribution it will be the mean)
    #variability_degradation_parameter - statistical distribution parameter that is linked to the variability (ex: for the normal distribution it will be the standard deviation)
    #degradation - simulated degradation
    #inspection - inspection peridiocity
    #time_maintenance_threshold - condition based maintenance threshold for the failure mode
    #condition_maintenance_threshold - condition based maintenance threshold for the failure mode
    #inspection_costs - inspection costs given the condition assessment
    #preventive_maintenance_costs - planned maintenance intervention costs
    #corrective_maintenance_costs - corrective maintenance intervention costs
    def __init__(self, initial_condition, failure_threshold, average_degradation_parameter, variability_degradation_parameter, degradation, inspection, time_maintenance_threshold,condition_maintenance_threshold, inspection_costs, preventive_maintenance_costs, corrective_maintenance_costs):

        self.initial_condition = initial_condition
        self.failure_threshold = failure_threshold
        self.average_degradation_parameter = average_degradation_parameter
        self.variability_degradation_parameter = variability_degradation_parameter
        self.degradation = list() if degradation is len(degradation)==0 else degradation
        self.inspection = inspection
        self.time_maintenance_threshold = time_maintenance_threshold
        self.condition_maintenance_threshold = condition_maintenance_threshold
        self.inspection_costs = inspection_costs
        self.preventive_maintenance_costs = preventive_maintenance_costs
        self.corrective_maintenance_costs = corrective_maintenance_costs

    #Function to clear the simulated degradation
    def clear_degradation(self):

        #delete the simulated degradation
        self.degradation = list()

    #Function to compute the failure mode MTBF depending on the selected process
    #Parameters:
    #degradation_process - We have to compute the mtbf according to degradation process: Gamma process or Wienner process
    def compute_mtbf(self, degradation_process):

        #Compute the mtbf based on a gamma process
        if degradation_process == 'gamma':
            #1-First we compute the birnbaum-saunders (bs) alpha parameter given the long-term gamma process
            bs_alpha = 1/((self.failure_threshold-self.initial_condition)/self.average_degradation_parameter)**0.5 #manual square root (i am trying to avoid importing libraries for this class)
            bs_beta = ((self.failure_threshold-self.initial_condition)/self.average_degradation_parameter)/self.variability_degradation_parameter

            #2-Then we compute the long-term failure mode MTBF
            return bs_beta*(1+bs_alpha**2/2)

        #Compute the mtbf based on a wienner process
        if degradation_process == 'wienner':
            return (self.failure_threshold-self.initial_condition)/self.average_degradation_parameter

        #This value implies that none of a method was correctly selected
        print("Choose either 'wienner' or 'gamma' to get a mtbf result.")
        return -1