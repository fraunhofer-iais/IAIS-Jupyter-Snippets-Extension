import scipy.stats as st
import pylab as pl
import numpy as np
from scipy import interpolate
import matplotlib.patches as mpatches

def outlier_1d(data, attribute, quantiles = [0.95, 0.9, 0.5]):
    colors = ['r']+[pl.cm.summer(q**2) for q in quantiles]

    # select the data
    x = data[attribute].values

    # calculate the borders
    span = abs(x.max()) - abs(x.min())
    minimum = x.min() - 0.2*span
    maximum = x.max() + 0.2*span
    stepsize = (maximum-minimum)/1000.
    positions = np.arange(minimum, maximum, stepsize)

    # Kernel Density Estimate
    kernel = st.gaussian_kde(x)
    z = kernel(positions)
    normfactor = z.sum()  
    z /= normfactor

    # Integral for each threshold
    t = np.linspace(0, z.max(), 1000)
    integral = ((z >= t[:, None]) * z).sum(axis=1)
    f = interpolate.interp1d(integral, t)

    # get the thresholds for the quantiles
    t_contours = f(quantiles).tolist()

    # plot the distribution and the quantiles
    fig = pl.figure(figsize=(10,5))
    ax = fig.gca()

    # plot the quantiles
    for i, val in enumerate(t_contours):
        ax.fill_between(positions, z, where=z>=val, color=colors[i+1])
    # plot the outliers
    ax.fill_between(positions, z, where=z<t_contours[0], color=colors[0])
    # plot the curve
    ax.plot(positions, z, color="#777777")
    # plot rug
    bottom = -0.1*max(z)
    ax.plot(x, [bottom]*len(x), '|', color='k', markersize=40, alpha=0.4)
    ax.axhline(0.0, color='k')

    ax.set_xlabel(attribute)
    ax.set_ylabel('P(%s)' %attribute)
    ax.set_xlim(minimum, maximum)
    ax.set_ylim(bottom, 1.1*max(z))

    # generate a nice legend
    patches = []
    for c in colors:
        patches.append(mpatches.Patch(color=c, linewidth=0))
    pl.legend(patches, ['Outliers']+["%d%%" %(q*100) for q in quantiles], loc='center left', bbox_to_anchor=(1, 0.5))
    pl.show()

    # outliers
    return data.ix[kernel(data[attribute])/normfactor < t_contours[0]]

