####################################################
###Funções dedicadas à análise de sensibilidade  ###
####################################################

#Required libraries
import numpy as np

from Asset_degradation import *

#Study the MTBF ratio between the short-term failure and long-term failure (Ratio = MTBF_st/MTBF_lt)
#Parameters:
#lt_failure_mode - Long term failure mode object that is used for the degradation process
#st_failure_mode - Short term failure mode object that is used for the degradation process
#sensitivity_step - The iterative step that we want when going through the interval
#maintenance_policy - Compute the costs according to the defined maintenance policy (CM - corrective maintenance, PM - perfect maintenance, TBM - time based maintenance, ICBM - with perfect inspection, CBM - with perfect continuous monitoring, EICBM - with imperfect inspection, ECBM - with imperfect continuous monitoring)
def failure_modes_mtbf_ratio(lt_failure_mode, st_failure_mode, sensitivity_step, maintenance_policy):

    #define the mtbf ratio that we want to study
    mtbf_ratio_interval = [ratio for ratio in range(0,1,sensitivity_step)]
    mtbf_ratio_interval.append(1) #garantuee that we add the maximum allowed value for the ratio

    #Colocar o cálculo do MTBF como uma função da classe!!!!!
    #Compute the new drift parameter (wienner process for the short-term) given the specified values of the ratio and predefined parameters
    #1-First we compute the birnbaum-saunders (bs) alpha parameter given the long-term gamma process
    bs_alpha = 1/np.sqrt((lt_failure_mode.failure_threshold-lt_failure_mode.initial_condition)/lt_failure_mode.average_degradation_parameter)
    bs_beta = ((lt_failure_mode.failure_threshold-lt_failure_mode.initial_condition)/lt_failure_mode.average_degradation_parameter)/lt_failure_mode.variability_degradation_parameter

    #2-Then we compute the long-term failure mode MTBF
    lt_mtbf = bs_beta*(1+bs_alpha^2/2)

    for ratio in mtbf_ratio_interval:

        #Calcular o drift que precisamos dado o rácio e mantendo o resto da informação
        st_failure_mode.average_degradation_parameter = (st_failure_mode.failure_threshold-st_failure_mode.initial_condition)/(ratio*lt_mtbf)

        #Simular a política de manutenção pretendida e guardar o melhor resultado (fiquei por aqui!!!!)