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
    #condition_maintenance_threshold - condition based maintenance threshold for the failure mode
    #inspection_costs - inspection costs given the condition assessment
    #preventive_maintenance_costs - planned maintenance intervention costs
    #corrective_maintenance_costs - corrective maintenance intervention costs
    def __init__(self, initial_condition, failure_threshold, average_degradation_parameter, variability_degradation_parameter, degradation, inspection, condition_maintenance_threshold, inspection_costs, preventive_maintenance_costs, corrective_maintenance_costs):

        self.initial_condition = initial_condition
        self.failure_threshold = failure_threshold
        self.average_degradation_parameter = average_degradation_parameter
        self.variability_degradation_parameter = variability_degradation_parameter
        self.degradation = list() if degradation is len(degradation)==0 else degradation
        self.inspection = inspection
        self.condition_maintenance_threshold = condition_maintenance_threshold
        self.inspection_costs = inspection_costs
        self.preventive_maintenance_costs = preventive_maintenance_costs
        self.corrective_maintenance_costs = corrective_maintenance_costs

    #Function to clear the simulated degradatin
    def clear_degradation(self):

        #delete the simulated degradation
        self.degradation = list()