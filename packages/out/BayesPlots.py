
import numpy as np
import matplotlib.pyplot as plt
from ..aux_funcs import reject_outliers
from . cornerPlot import hist2d


def histogram(
    gs, gsx, gsy, mcmc_samples, _16_50_84_mean_mode, mu_x_kde,
        xylabel, dec_places):
    """
    Parameter's distribution
    """
    # Histogram
    ax = plt.subplot(gs[gsy[0]:gsy[1], gsx[0]:gsx[1]])
    plt.xlabel(xylabel, fontsize=11)
    no_outlr = reject_outliers(mcmc_samples.flatten())
    # Obtain the bin edges.
    hist, bin_edges = np.histogram(no_outlr, bins=25)
    # Plot bars with the proper positioning, height, and width.
    plt.bar(
        (bin_edges[1:] + bin_edges[:-1]) * .5, hist / float(hist.max()),
        width=(bin_edges[1] - bin_edges[0]), color='grey', alpha=0.3)
    # Plot KDE.
    plt.plot(mu_x_kde[0], mu_x_kde[1] / max(mu_x_kde[1]), color='k', lw=1.5)

    _16, _50, _84, _mean, _mode = _16_50_84_mean_mode

    # Mean
    plt.axvline(
        x=_mean, linestyle='--', color='blue', zorder=4,
        label=("Mean (" + dec_places + ")").format(_mean))
    # Median
    plt.axvline(
        x=_50, linestyle='--', color='green', zorder=4,
        label=("Median (" + dec_places + ")").format(_50))
    # Mode
    plt.axvline(
        x=_mode, linestyle='--', color='cyan', zorder=4,
        label=("Mode (" + dec_places + ")").format(_mode))

    # 16th and 84th percentiles.
    std = np.std(mcmc_samples.flatten())
    txt = "16-84th perc\n" +\
        (r"$(" + dec_places + ", " + dec_places + ")$").format(_16, _84)
    plt.axvline(
        x=_16, linestyle=':', color='orange', zorder=4, label=txt)
    plt.axvline(x=_84, linestyle=':', color='orange', zorder=4)

    plt.xlim(max(-1., (_mean) - 4. * std), (_mean) + 4. * std)
    cur_ylim = ax.get_ylim()
    ax.set_ylim([0, cur_ylim[1]])
    plt.legend()


def traceplot(
    gs, gsx, gsy, mcmc_samples, _16_50_84_mean_mode, Brn_prcnt, xylabel,
        xticks=True):
    """
    Chains traceplot.
    """
    ax = plt.subplot(gs[gsy[0]:gsy[1], gsx[0]:gsx[1]])
    N_tot = mcmc_samples.shape[0]
    plt.plot(mcmc_samples, c='k', lw=.8, ls='-', alpha=0.5)
    Nburn = Brn_prcnt * N_tot
    plt.axvline(x=Nburn, linestyle=':', color='r', zorder=4)
    # 16th and 84th percentiles + median.
    plt.axhline(
        y=_16_50_84_mean_mode[0], linestyle=':', color='orange', zorder=4)
    plt.axhline(
        y=_16_50_84_mean_mode[3], linestyle=':', color='blue', zorder=4)
    plt.axhline(
        y=_16_50_84_mean_mode[2], linestyle=':', color='orange', zorder=4)
    if xticks is True:
        plt.xlabel("Steps")
    else:
        plt.xticks([])
    plt.ylabel(xylabel)
    # Use the last 10% of the chains.
    N = int(mcmc_samples.shape[0] * .1)
    std = np.std(mcmc_samples[-N:])
    pmin, pmax = np.min(mcmc_samples[-N:]), np.max(mcmc_samples[-N:])
    ymin, ymax = pmin - std, pmax + std
    ax.set_ylim(ymin, ymax)
    ax.set_xlim(0, N_tot)


def autocorr(gs, gsx, gsy, Nsteps, tau_autocorr, ESS):
    """
    Mean autocorrelation time.
    """
    plt.subplot(gs[gsy[0]:gsy[1], gsx[0]:gsx[1]])
    plt.plot(
        Nsteps * np.arange(tau_autocorr.size), tau_autocorr,
        label=r"$N_{{ESS}}\approx${:.0f}".format(ESS))
    plt.xlabel("Steps")
    plt.ylabel(r"$\hat{\tau}$")
    plt.legend()


def meanAF(gs, gsx, gsy, Nsteps, mean_afs):
    """
    Mean acceptance fraction.
    """
    plt.subplot(gs[gsy[0]:gsy[1], gsx[0]:gsx[1]])
    plt.plot(Nsteps * np.arange(mean_afs.size), mean_afs,
             label=r"$MAF\approx${:.2f}".format(mean_afs[-1]))
    plt.xlabel("Steps")
    plt.ylabel(r"$MAF$")
    plt.legend()


def twoParDens(
        gs, gsx, gsy, x_samples, y_samples, KP_Bys_rc, KP_Bys_rt, xylabel):
    """
    """
    ax = plt.subplot(gs[gsy[0]:gsy[1], gsx[0]:gsx[1]])
    hist2d(ax, x_samples, y_samples)
    plt.scatter(
        KP_Bys_rc[1], KP_Bys_rt[1], marker='x', c='green', s=50, zorder=5)
    plt.scatter(
        KP_Bys_rc[3], KP_Bys_rt[3], marker='x', c='blue', s=50, zorder=5)
    plt.scatter(
        KP_Bys_rc[4], KP_Bys_rt[4], marker='x', c='cyan', s=50, zorder=5)

    plt.xlabel(xylabel[0])
    plt.ylabel(xylabel[1])

    xl, yl = ax.get_xlim(), ax.get_ylim()
    xmed, xstd = np.median(x_samples), np.std(x_samples)
    ymed, ystd = np.median(y_samples), np.std(y_samples)
    x3s_min, x3s_max = xmed - 3. * xstd, xmed + 3. * xstd
    y3s_min, y3s_max = ymed - 3. * ystd, ymed + 3. * ystd
    plt.xlim(max(xl[0], x3s_min), min(xl[1], x3s_max))
    plt.ylim(max(yl[0], y3s_min), min(yl[1], y3s_max))
