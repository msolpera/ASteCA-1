# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 16:10:05 2014

@author: gabriel
"""

from genetic_algorithm import gen_algor as g_a
from brute_force_algorithm import brute_force as b_f
from bootstrap_func import bootstrap
from synth_cluster import synth_clust as s_c
from error_round import round_sig_fig as rsf
from get_IMF_PDF import IMF_PDF as i_p
from move_isochrone import move_isoch
import numpy as np


def best_fit(err_lst, memb_prob_avrg_sort, completeness, ip_list, bf_params,
             sc_params, ga_params, ps_params):
    '''
    Perform a best fitting process to find the cluster's parameters:
    E(B-V), distance (distance modulus), age and metallicity.
    '''

    bf_flag, best_fit_algor, N_b = bf_params
    cmd_sel = ps_params[1]

    # Check if algorithm should run.
    if bf_flag:

        print 'Searching for optimal parameters.'

        # Obtain the selected IMF's PDF. We run it once because the array only
        # depends on the IMF selected.
        imf_pdf = i_p(sc_params[0])
        # Replace the name of the IMF by its PDF.
        sc_params[0] = imf_pdf

        # Call algorithm to calculate the likelihoods for the set of
        # isochrones and return the best fitting parameters.
        if best_fit_algor == 'brute':

            print 'Using Brute Force algorithm.'
            # Brute force algorithm.
            isoch_fit_params = b_f(err_lst, memb_prob_avrg_sort, completeness,
                                   ip_list, sc_params, ga_params, cmd_sel)
            # Assign errors as the steps in each parameter.
            isoch_fit_errors = [ps_params[i + 3][2] for i in range(4)]

        elif best_fit_algor == 'genet':

            print 'Using Genetic Algorithm.'
            # Genetic algorithm.
            # Let the GA algor know this call comes from the main function
            # so it will print percentages to screen.
            flag_print_perc = True
            # Remove IDs so likelihood function works.
            obs_clust = np.array(zip(*zip(*memb_prob_avrg_sort)[1:]),
                dtype=float)
            isoch_fit_params = g_a(flag_print_perc, err_lst,
                obs_clust, completeness, ip_list, sc_params,
                ga_params, cmd_sel)

        print 'Best fit params obtained ({:g}, {:g}, {:g}, {:g}).'.format(
            isoch_fit_params[0][0], isoch_fit_params[0][1],
            isoch_fit_params[0][2], isoch_fit_params[0][3])

        if best_fit_algor == 'genet':
            if N_b >= 2:
                # Call bootstrap function with resampling to get the uncertainty
                # in each parameter.
                isoch_fit_errors = bootstrap(err_lst, obs_clust, completeness,
                    ip_list, bf_params, sc_params, ga_params, ps_params)

                # Round errors to 1 significant digit and round params values
                # to the corresponding number of significant digits given by
                # the errors.
                isoch_fit_params[0], isoch_fit_errors = rsf(isoch_fit_params[0],
                    isoch_fit_errors)
            else:
                print 'Skipping bootstrap process.'
                isoch_fit_errors = [-1.] * 4

        # For plotting purposes.
        # Get list of stored isochrones and their parameters.
        isoch_list, param_values = ip_list[0], ip_list[1]
        # Read best fit values for all parameters.
        m, a, e, d = isoch_fit_params[0]
        # Find indexes for metallicity and age. If indexes are not found due
        # to some difference in the significant figures, use the indices
        # [0, 0] to prevent the code from halting.

        #m_indx, a_indx = next(((i, j) for i, x in enumerate(isoch_ma) for j, y
        #in enumerate(x) if y == [m, a]), [0, 0])

        try:
            m_i, a_i = param_values[0].index(m), param_values[1].index(a)
        except:
            m_i, a_i = [0, 0]

        # Generate shifted best fit isochrone.
        shift_isoch = move_isoch(cmd_sel, isoch_list[m_i][a_i][:2], e, d)
        # Generate best fit synthetic cluster.
        synth_clst = s_c(err_lst, completeness, sc_params,
                         isoch_list[m_i][a_i], [-1., -1., e, d], cmd_sel)

    else:
        # Pass empty lists to make_plots.
        print 'Skipping parameters fitting process.'
        isoch_fit_params, isoch_fit_errors, shift_isoch, synth_clst = \
        [[-1., -1., -1., -1.]], [-1., -1., -1., -1.], [], []

    bf_return = [isoch_fit_params, isoch_fit_errors, shift_isoch, synth_clst]

    return bf_return