
import time as t
# from .sampyl.samplers import NUTS as smpNUTS
from .sampyl.samplers.slice import Slice
from ..core_imp import np
from .emcee_algor import varPars, log_posterior, convergenceVals, closeSol


class Target():
    def __init__(self, priors, varIdxs, ranges, fundam_params, synthcl_args,
                 lkl_method, obs_clust):
        self.priors = priors
        self.varIdxs = varIdxs
        self.ranges = ranges
        self.fundam_params = fundam_params
        self.synthcl_args = synthcl_args
        self.lkl_method = lkl_method
        self.obs_clust = obs_clust

    def logpdf(self, x):
        model_done = {}
        # model = [met, age, ext, dist, mass, binar]
        lp = log_posterior(
            x, self.priors, self.varIdxs, self.ranges, self.fundam_params,
            self.synthcl_args, self.lkl_method, self.obs_clust, model_done)
        # The log_posterior returns a value (log_prior+log_posterior) that
        # needs to be maximized.
        return lp

    def __call__(self, x):
        return self.logpdf(x)


def main(
    lkl_method, e_max, err_lst, completeness, max_mag_syn,
        fundam_params, obs_clust, theor_tracks, R_V, ext_coefs, st_dist_mass,
        N_fc, cmpl_rnd, err_rnd, nwalkers, nsteps, nburn, N_burn,
        emcee_a, priors):
    """
    """
    varIdxs, ndim, ranges = varPars(fundam_params)

    synthcl_args = [
        theor_tracks, e_max, err_lst, completeness, max_mag_syn, st_dist_mass,
        R_V, ext_coefs, N_fc, cmpl_rnd, err_rnd]

    # Thinly-wrapped numpy
    # import autograd.numpy as np
    # The only autograd function you may ever need
    # from autograd import grad
    # #
    # grad_logp = grad(logp)       # Obtain its gradient function
    # grad_logp(.03, 9.7, 0.3, 12.7, 5000., .3)

    # bounds = {
    #     'met': ranges[0], 'age': ranges[1], 'ext': ranges[2],
    #     'dist': ranges[3], 'mass': ranges[4], 'binar': ranges[5]}
    # start = smp.find_MAP(logp, {
    #     'met': .015, 'age': 9., 'ext': 0., 'dist': 13., 'mass': 5000.,
    #     'binar': .3}, verbose=True, bounds=bounds)

    start = {
        'met': .03, 'age': 9.7, 'ext': 0.3, 'dist': 12.7, 'mass': 5000.,
        'binar': .3}
    # start = {'ext': 0.3, 'dist': 12.7, 'mass': 5000., 'binar': .3}

    s = t.time()
    # sampler = NUTS(logp, start)
    # sampler = Slice(logp, start)
    logp = Target(priors, varIdxs, ranges, fundam_params, synthcl_args,
                  lkl_method, obs_clust)
    sampler = Slice(logp, start)

    # TODO SLICE SAMPLER DOES NOT ACCEPT MORE THAN 1 CHAIN
    burn_in = sampler.sample(nburn, n_chains=nburn)
    pars_chains_bi = np.array([
        burn_in.met, burn_in.age, burn_in.ext, burn_in.dist, burn_in.mass,
        burn_in.binar])
    # pars_chains_bi = pars_chains_bi[:, np.newaxis, :]

    start = {
        'met': burn_in.met[-1], 'age': burn_in.age[-1], 'ext': burn_in.ext[-1],
        'dist': burn_in.dist[-1], 'mass': burn_in.mass[-1],
        'binar': burn_in.binar[-1]}
    sampler = Slice(logp, start)
    chain = sampler.sample(nsteps, n_chains=nwalkers)

    # (nsteps, nwalkers, ndim)
    chains_nruns = np.array([
        chain.met, chain.age, chain.ext, chain.dist, chain.mass,
        chain.binar]).T
    # chains_nruns = chains_nruns[:, np.newaxis, :]

    # (ndim, nsteps * nwalkers)
    mcmc_trace = chains_nruns.reshape(-1, ndim).T
    elapsed = t.time() - s

    N_conv, N_steps_conv, tol_conv, runs = 0., nsteps, 0., nsteps
    map_sol, map_lkl, map_lkl_final = [np.nan] * 6, [[0., 0.]], np.nan
    maf_steps = [[0., 0.]]
    tau_index, tau_autocorr = 0, np.empty(nsteps)

    # Convergence parameters.
    acorr_t, max_at_5c, min_at_5c, geweke_z, emcee_acorf, pymc3_ess, minESS,\
        mESS, mESS_epsilon, mcmc_halves = convergenceVals(
            ndim, varIdxs, N_conv, chains_nruns, mcmc_trace)

    # Pass the mean as the best model fit found.
    best_sol = closeSol(fundam_params, varIdxs, np.mean(mcmc_trace, axis=1))

    isoch_fit_params = {
        'varIdxs': varIdxs, 'nsteps': runs, 'best_sol': best_sol,
        'map_sol': map_sol, 'map_lkl': map_lkl, 'map_lkl_final': map_lkl_final,
        'mcmc_elapsed': elapsed, 'mcmc_trace': mcmc_trace,
        'pars_chains_bi': pars_chains_bi, 'pars_chains': chains_nruns.T,
        'maf_steps': maf_steps, 'autocorr_time': acorr_t,
        'max_at_5c': max_at_5c, 'min_at_5c': min_at_5c,
        'minESS': minESS, 'mESS': mESS, 'mESS_epsilon': mESS_epsilon,
        'emcee_acorf': emcee_acorf, 'geweke_z': geweke_z,
        'pymc3_ess': pymc3_ess, 'mcmc_halves': mcmc_halves,
        'N_steps_conv': N_steps_conv, 'N_conv': N_conv, 'tol_conv': tol_conv,
        'tau_index': tau_index, 'tau_autocorr': tau_autocorr
    }

    return isoch_fit_params
