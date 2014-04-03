"""
@author: gabriel
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def disp_rad(phot_data, center_params, clust_rad, delta_backg, delta_percentage,
            backg_value, rdp_params):
    '''
    Plot cluster and its radius.
    '''

    # Unpack.
    x_data, y_data, mag_data, col1_data = phot_data[1], phot_data[2], \
    phot_data[3], phot_data[5]
    center_cl, h_not_filt, x_center_bin, y_center_bin, xedges_min_db, \
    yedges_min_db, bin_width, h_filter, cent_cl_err = center_params[:9]
    radii, ring_density, poisson_error = rdp_params

    # Plot all outputs
    fig = plt.figure(figsize=(12, 12))
    gs = gridspec.GridSpec(2, 2)  # create a GridSpec object

    # 2D filtered histogram, smallest bin width.
    ax1 = plt.subplot(gs[0, 0])
    plt.xlabel('x (bins)', fontsize=12)
    plt.ylabel('y (bins)', fontsize=12)
    ax1.minorticks_on()
    plt.axvline(x=x_center_bin, linestyle='--', color='white')
    plt.axhline(y=y_center_bin, linestyle='--', color='white')
    # Radius
    circle = plt.Circle((x_center_bin, y_center_bin),
        clust_rad / bin_width, color='w', fill=False)
    fig.gca().add_artist(circle)
    #text = 'Center (%d, %d)' % (x_center_bin, y_center_bin)
    text = 'Bin: %d px' % (bin_width)
    plt.text(0.7, 0.92, text, transform=ax1.transAxes,
             bbox=dict(facecolor='white', alpha=0.8), fontsize=12)
    plt.imshow(h_filter[0].transpose(), origin='lower')

    ax2 = plt.subplot(gs[0, 1])
    # Get max and min values in x,y
    x_min, x_max = min(x_data), max(x_data)
    y_min, y_max = min(y_data), max(y_data)
    #Set plot limits
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    #Set axis labels
    plt.xlabel('x (px)', fontsize=12)
    plt.ylabel('y (px)', fontsize=12)
    # Set minor ticks
    ax2.minorticks_on()
    circle = plt.Circle((center_cl[0], center_cl[1]), clust_rad, color='r',
                        fill=False)
    fig.gca().add_artist(circle)
    # Add text box
    text1 = '$x_{cent} = %d \pm %d px$' % (center_cl[0], cent_cl_err[0])
    text2 = '\n'
    text3 = '$y_{cent} = %d \pm %d px$' % (center_cl[1], cent_cl_err[1])
    text4 = text1 + text2 + text3
    plt.text(0.5, 0.85, text4, transform=ax2.transAxes,
        bbox=dict(facecolor='white', alpha=0.85), fontsize=15)
    # Plot stars.
    a, b, c = 50, -0.003, 2.5
    plt.scatter(x_data, y_data, marker='o', c='black',
        s=a * np.exp(b * mag_data ** c))

    ax3 = plt.subplot(gs[1, 0:2])
    # Get max and min values in x,y
    x_max = max(radii) + 10
    y_min, y_max = (backg_value - delta_backg) - (max(ring_density) -
    min(ring_density)) / 10, max(ring_density) + (max(ring_density) -
    min(ring_density)) / 10
    # Set plot limits
    plt.xlim(-10, x_max)
    plt.ylim(y_min, y_max)
    # Set axes labels
    plt.xlabel('radius (px)', fontsize=12)
    plt.ylabel("stars/px$^{2}$", fontsize=12)
    # Cluster's name.
    #text = str(clust_name)
    #plt.text(0.4, 0.9, text, transform=ax3.transAxes, fontsize=14)
    # Legend texts
    texts = ['Dens prof (%d px)' % bin_width,
            'backg = %.1E $st/px^{2}$' % backg_value,
            '$\Delta$=%d%%' % delta_percentage,
            'r$_{cl}$ = %d $\pm$ %d px' % (clust_rad, round(bin_width))]
    # Plot density profile with the smallest bin size
    ax3.plot(radii, ring_density, 'ko-', zorder=3, label=texts[0])
    # Plot poisson error bars
    plt.errorbar(radii, ring_density, yerr=poisson_error, fmt='ko',
                 zorder=1)
    # Plot background level.
    ax3.hlines(y=backg_value, xmin=0, xmax=max(radii),
               label=texts[1], color='b', zorder=5)
    # Plot the delta around the background value used to asses when the density
    # has become stable
    plt.hlines(y=(backg_value + delta_backg), xmin=0, xmax=max(radii),
               color='b', linestyles='dashed', label=texts[2], zorder=2)
    # Approx middle of the graph.
    arr_y_up = (y_max - y_min) / 2.3 + y_min
    # Length of arrow head.
    #head_w = abs((arr_y_up - backg_value) / 10.)
    head_w, head_l = x_max * 0.023, (y_max - y_min) * 0.045
    # Length of arrow.
    arr_y_dwn = -1. * abs(arr_y_up - backg_value) * 0.76
    # Plot radius.
    ax3.vlines(x=clust_rad, ymin=0, ymax=0., label=texts[3], color='r')
    ax3.arrow(clust_rad, arr_y_up, 0., arr_y_dwn, fc="r",
              ec="r", head_width=head_w, head_length=head_l, zorder=5)
    # get handles
    handles, labels = ax3.get_legend_handles_labels()
    # use them in the legend
    ax3.legend(handles, labels, loc='upper right', numpoints=2, fontsize=12)
    ax3.minorticks_on()

    plt.draw()
    print 'Plot displayed, waiting for it to be closed.'
