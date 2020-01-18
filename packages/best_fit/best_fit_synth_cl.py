
from ..core_imp import np
from . import max_mag_cut, obs_clust_prepare, bootstrap, ptemcee_algor
from . import emcee_algor
# brute_force_algor , abcpmc_algor,
# TODO in place for #397: hopp_algor
from ..synth_clust import extin_coefs
from ..synth_clust import imf


def main(clp, pd):
    """
    Perform a best fitting process to find the cluster's fundamental
    parameters.
    """

    # Check if algorithm should run.
    if pd['bf_flag']:

        # Remove stars beyond the maximum magnitude limit, if it was set.
        cl_max_mag, max_mag_syn = max_mag_cut.main(
            clp['cl_reg_fit'], pd['max_mag'])

        # Processed observed cluster.
        obs_clust = obs_clust_prepare.main(
            cl_max_mag, pd['lkl_method'], pd['lkl_binning'],
            pd['lkl_manual_bins'])

        # Obtain extinction coefficients.
        # This parameter determines the total number of sub-arrays for each
        # isochrone stored.
        ext_shape = len(pd['theor_tracks'][0][0])
        ext_coefs = extin_coefs.main(
            pd['cmd_systs'], pd['filters'], pd['colors'], ext_shape)

        # Obtain mass distribution using the selected IMF. We run it once
        # because the array only depends on the IMF selected.
        st_dist_mass = imf.main(pd['IMF_name'], pd['fundam_params'][4])

        # Store the number of defined filters and colors.
        N_fc = [len(pd['filters']), len(pd['colors'])]

        # Generate required parameters to use in the error adding function.
        # HARDCODED this assumes that there will never be more than 1e6 stars
        # in a synthetic cluster
        N_errors = 1000000
        if pd['lkl_method'] == 'tolstoy':
            err_rand = np.zeros(N_errors)
        else:
            err_rand = np.random.normal(0., 1., N_errors)
        err_pars = clp['err_lst'], clp['em_float'], err_rand

        # # TEMPORARY
        # # Use for saving the necessary input for the 'perf_test.py' file.
        # import pickle
        # with open('perf_test.pickle', 'wb') as f:
        #     pickle.dump([
        #         obs_clust, cl_max_mag, pd['fundam_params'], pd['theor_tracks'],
        #         pd['lkl_method'], pd['R_V'], clp['completeness'],
        #         max_mag_syn, st_dist_mass, ext_coefs, N_fc, pd['m_ini_idx'],
        #         pd['binar_flag'], err_pars], f)
        # print("finished")
        # import sys
        # sys.exit()
        # # TEMPORARY

        clp['max_mag_syn'], clp['ext_coefs'], clp['st_dist_mass'],\
            clp['N_fc'], clp['err_pars'], = max_mag_syn, ext_coefs,\
            st_dist_mass, N_fc, err_pars

        print("Searching for optimal parameters")

        # Calculate the best fitting parameters.
        if pd['best_fit_algor'] == 'ptemcee':
            print("Using ptemcee algorithm ({})".format(
                pd['lkl_method'] + '; ' + pd['lkl_binning'] if
                pd['lkl_method'] in ('dolphin', 'tremmel') else
                pd['lkl_method']))

            isoch_fit_params = ptemcee_algor.main(
                clp['completeness'], max_mag_syn, obs_clust, ext_coefs,
                st_dist_mass, N_fc, err_pars, **pd)
            # Assign uncertainties.
            isoch_fit_errors = params_errors(pd, isoch_fit_params)

        elif pd['best_fit_algor'] == 'boot+GA':

            print("Using bootstrap + Genetic Algorithm ({})".format(
                pd['lkl_method'] + '; ' + pd['lkl_binning'] if
                pd['lkl_method'] in ('dolphin', 'tremmel') else
                pd['lkl_method']))
            isoch_fit_params = bootstrap.main(
                pd, clp, cl_max_mag, max_mag_syn, obs_clust, ext_coefs,
                st_dist_mass, N_fc, err_pars)
            # Assign uncertainties.
            isoch_fit_errors = params_errors(pd, isoch_fit_params)

        elif pd['best_fit_algor'] == 'emcee':
            print('Using emcee algorithm ({}).'.format(
                pd['lkl_method'] + '; ' + pd['lkl_binning'] if
                pd['lkl_method'] in ('dolphin', 'tremmel') else
                pd['lkl_method']))
            isoch_fit_params = emcee_algor.main(
                clp['err_lst'], clp['completeness'], clp['em_float'],
                max_mag_syn, obs_clust, ext_coefs, st_dist_mass, N_fc,
                err_pars, **pd)
            # Assign uncertainties.
            isoch_fit_errors = params_errors(pd, isoch_fit_params)

        # TODO DEPRECATED May 2019
        # if best_fit_algor == 'brute':
        #     print('Using Brute Force algorithm ({}).'.format(
        #         lkl_method + '; ' + lkl_binning if lkl_method == 'dolphin'
        #         else lkl_method))
        #     # Brute force algorithm.
        #     isoch_fit_params = brute_force_algor.main()

        # TODO not working yet
        # elif best_fit_algor == 'abc':
        #     print('Using abcpmc algorithm ({}).'.format(
        #         lkl_method + '; ' + lkl_binning if lkl_method == 'dolphin'
        #         else lkl_method))
        #     isoch_fit_params = abcpmc_algor.main()
        #     # Assign uncertainties.
        #     isoch_fit_errors, _ = params_errors(
        #         best_fit_algor, isoch_fit_params)

        print("Best fit parameters obtained")

    else:
        print("Skip parameters fitting process")
        # Pass dummy data used by data output and some plot functions.
        cl_max_mag, obs_clust = [], [[]]
        isoch_fit_params = {
            'mean_sol': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            'median_sol': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            'map_sol': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            'mode_sol': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            'param_r2': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            'N_total': np.nan}
        isoch_fit_errors = [[np.nan, np.nan, np.nan]] * 6

    clp['cl_max_mag'], clp['bf_bin_edges'], clp['isoch_fit_params'],\
        clp['isoch_fit_errors'] = cl_max_mag, obs_clust[0], isoch_fit_params,\
        isoch_fit_errors

    return clp


def params_errors(pd, isoch_fit_params):
    '''
    Obtain uncertainties for the fitted parameters.
    '''
    # DEPRECATED May 2019
    # if best_fit_algor == 'brute':
    #     fundam_params = args
    #     isoch_fit_errors = []
    #     # Assign errors as the largest step in each parameter.
    #     for pv in fundam_params:
    #         # If any parameter has a single valued range, assign 'nan'.
    #         if len(pv) > 1:
    #             # Find largest delta in this parameter used values.
    #             largest_delta = np.diff(pv).max()
    #             # Store the maximum value.
    #             isoch_fit_errors.append(largest_delta)
    #         else:
    #             isoch_fit_errors.append(np.nan)

    def assignUncertns(varIdxs, trace):
        isoch_fit_errors, j = [], 0
        for i in range(6):
            if i in varIdxs:
                # 16th and 84th percentiles (1 sigma), and STDDEV
                ph = np.percentile(trace[i - j], 84)
                pl = np.percentile(trace[i - j], 16)
                std = np.std(trace[i - j])
                isoch_fit_errors.append((pl, ph, std))
            else:
                isoch_fit_errors.append((np.nan, np.nan, np.nan))
                j += 1

        return isoch_fit_errors

    if pd['best_fit_algor'] in ('boot+GA'):

        pb = isoch_fit_params['params_boot']
        if pb.any():
            isoch_fit_errors = assignUncertns(isoch_fit_params['varIdxs'], pb)
        else:
            # No error assignment.
            isoch_fit_errors = [[np.nan] * 3] * 6

    elif pd['best_fit_algor'] in ('ptemcee', 'emcee'):  # , , 'abc'
        isoch_fit_errors = assignUncertns(
            isoch_fit_params['varIdxs'], isoch_fit_params['mcmc_trace'])

    return isoch_fit_errors
