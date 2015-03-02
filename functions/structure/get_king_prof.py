# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 10:54:00 2013

@author: gabriel
"""

import numpy as np
from scipy.optimize import curve_fit
import king_prof_funcs as kpf
from .._in import get_in_params as g


def get_king_profile(clust_rad, field_dens, radii, ring_density):
    '''
    Function to fit the 3-params King profile to a given radial density.
    The field density value is fixed and the core radius, tidal radius and
    maximum central density are fitted.
    '''

    coord = g.gd_params[-1][0]
    # Flags that indicate either no convergence or that the fits were not
    # attempted.
    flag_2pk_conver, flag_3pk_conver = False, False

    # Initial dummy values
    rc, e_rc, rt, e_rt, n_c_k, kcp, cd = -1., -1., -1., -1., -1., -1., -1.

    # Check flag to run or skip.
    if g.kp_flag:

        # Field density value is fixed.
        fd = field_dens
        # Initial guesses for fit: max_dens, rt, rc
        max_dens, rt, rc = max(ring_density), clust_rad, clust_rad / 2.
        guess2 = (max_dens, rc)
        guess3 = (max_dens, rc, rt)

        # Skip first radius value if it is smaller than the second value. This
        # makes it easier for the KP to converge.
        if ring_density[0] > ring_density[1]:
            radii_k, ring_dens_k = radii, ring_density
        else:
            radii_k, ring_dens_k = radii[1:], ring_density[1:]

        # Attempt to fit a 3-P King profile with the background value fixed.
        try:
            popt, pcov = curve_fit(lambda x, cd, rc,
                rt: kpf.three_params(x, rt, cd, rc, fd), radii_k, ring_dens_k,
                guess3)

            # Unpack tidal radius and its error.
            cd, rc, rt = popt
            e_rc = np.sqrt(pcov[1][1]) if pcov[1][1] > 0 else -1.
            e_rt = np.sqrt(pcov[2][2]) if pcov[2][2] > 0 else -1.
            flag_3pk_conver = True

            # If fit converged to tidal radius that extends beyond 100 times
            # the core radius, or either radius is equal or less than zero;
            # discard the fit.
            if rt > rc * 100. or rt <= 0. or rc <= 0.:
                # Raise flag to reject fit.
                flag_3pk_conver = False
        except:
            flag_3pk_conver = False

        # If 3-P King profile converged, ie: the tidal radius was found,
        # calculate approximate number of cluster members with eq (3) from
        # Froebrich et al. (2007); 374, 399-408 and the concentration parameter.
        if flag_3pk_conver:
            print 'Tidal radius obtained: {:g} {}.'.format(rt, coord)
            # Obtain approximate number of members.
            x = 1 + (rt / rc) ** 2
            n_c_k = int(round((np.pi * cd * rc ** 2) * (np.log(x) -
            4 + (4 * np.sqrt(x) + (x - 1)) / x)))
            # Obtain concentration parameter.
            kcp = np.log10(rt / rc)
        else:
            # If 3-param King fit did not converge.
            print '  WARNING: tidal radius could not be obtained.'
            # If 3-P King profile did not converge, pass dummy values
            rt, e_rt, n_c_k, kcp = -1., -1., -1., -1.

            # Fit a 2P King profile first to obtain the maximum central
            # density and core radius.
            try:
                popt, pcov = curve_fit(lambda x, cd,
                    rc: kpf.two_params(x, cd, rc, fd), radii_k, ring_dens_k,
                    guess2)
                # Unpack max density and core radius.
                cd, rc = popt
                # Obtain error in core radius.
                if np.isfinite(pcov).all():
                    e_rc = np.sqrt(pcov[1][1]) if pcov[1][1] > 0 else -1.
                else:
                    e_rc = -1.
                flag_2pk_conver = True
            except:
                flag_2pk_conver = False
                # Pass dummy values
                rc, e_rc, cd = -1., -1., -1.

            # If 2-param converged to zero or negative core radius.
            if rc <= 0:
                flag_2pk_conver = False
                # Pass dummy values
                rc, e_rc, rt, e_rt, n_c_k, kcp, cd = -1., -1., -1., -1., -1., \
                -1., -1.

            if flag_2pk_conver is False:
                print '  WARNING: core radius could not be obtained.'

    return rc, e_rc, rt, e_rt, n_c_k, kcp, cd, flag_2pk_conver, flag_3pk_conver