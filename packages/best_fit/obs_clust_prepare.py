
import numpy as np
from ..decont_algors.local_cell_clean import bin_edges_f


def main(cl_reg_fit, lkl_method, bin_method):
    '''
    Prepare observed cluster array here to save time before the algorithm to
    find the best synthetic cluster fit is used.
    '''

    # Extract photometric data, and membership probabilities. Remove ID's to
    # make entire array of floats.
    mags_cols_cl = [[], []]
    for mag in zip(*zip(*cl_reg_fit)[1:][2]):
        mags_cols_cl[0].append(mag)
    for col in zip(*zip(*cl_reg_fit)[1:][4]):
        mags_cols_cl[1].append(col)

    # Square errors here to not repeat the same calculations each time a
    # new synthetic cluster is matched.
    e_mags_cols = []
    for e_m in zip(*zip(*cl_reg_fit)[1:][3]):
        e_mags_cols.append(np.square(e_m))
    for e_c in zip(*zip(*cl_reg_fit)[1:][5]):
        e_mags_cols.append(np.square(e_c))

    # Store membership probabilities here.
    probs = np.array(zip(*cl_reg_fit)[1:][6])

    if lkl_method == 'tolstoy':
        # Store and pass to use in likelihood function. The 'all_st' list is
        # made up of:
        # all_st = [star_1, star_2, ...]
        # star_i = [phot_1, phot_2, phot_3, ...]
        # phot_j = [phot_val, error]
        # Where 'phot_j' is a photometric dimension (magnitude or color), and
        # 'phot_val', 'error' the associated value and error for 'star_i'.
        all_st = []
        mags_cols = mags_cols_cl[0] + mags_cols_cl[1]
        for st_phot, st_e_phot in zip(zip(*mags_cols), zip(*e_mags_cols)):
            all_st.append(zip(*[st_phot, st_e_phot]))
        obs_clust = [all_st, probs]

    else:
        # Obtain bin edges for each dimension, defining a grid.
        bin_edges = bin_edges_f(bin_method, mags_cols_cl)

        # Obtain *weighted* histogram for observed cluster. Put all magnitudes
        # and colors into a single list.

        # TODO Owing to #308 I've removed 'weights=prob' from histogramdd,
        # until I have time to make more tests.

        cl_histo = np.histogramdd(
            mags_cols_cl[0] + mags_cols_cl[1], bins=bin_edges)[0]

        # Flatten N-dimensional histogram.
        cl_histo_f = np.array(cl_histo).ravel()
        # Remove all bins where n_i = 0 (no observed stars).
        cl_z_idx = [cl_histo_f != 0]
        cl_histo_f = cl_histo_f[cl_z_idx]

        # Store and pass to use in likelihood function.
        # 'cl_histo' is used to obtain the Hess diagram when plotting.
        obs_clust = [cl_histo_f, cl_z_idx, bin_edges, cl_histo]

    return obs_clust
