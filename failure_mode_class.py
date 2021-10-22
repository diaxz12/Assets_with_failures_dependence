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
    #preventive_maintenance_costs - planned maintenance intervention costs
    #corrective_maintenance_costs - corrective maintenance intervention costs
    def __init__(self, initial_condition, failure_threshold, average_degradation_parameter, variability_degradation_parameter, degradation, preventive_maintenance_costs, corrective_maintenance_costs):

        self.initial_condition = initial_condition
        self.failure_threshold = failure_threshold
        self.average_degradation_parameter = average_degradation_parameter
        self.variability_degradation_parameter = variability_degradation_parameter
        self.degradation = list() if degradation is len(degradation)==0 else degradation
        self.preventive_maintenance_costs = preventive_maintenance_costs
        self.corrective_maintenance_costs = corrective_maintenance_costs