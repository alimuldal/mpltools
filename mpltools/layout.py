import numpy as np
import matplotlib.pyplot as plt


__all__ = ['clear_frame', 'figimage', 'cross_spines', 'pad_limits']


def clear_frame(ax=None):
    """Remove the frame (ticks and spines) from an axes.

    This differs from turning off the axis (`plt.axis('off')` or
    `ax.set_axis_off()`) in that only the ticks and spines are removed. Turning
    off the axis also removes the axes background and axis labels.

    Parameters
    ----------
    ax : :class:`~matplotlib.axes.Axes`
        Axes to modify. If None, use current axes.
    """
    ax = ax if ax is not None else plt.gca()

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    for spine in ax.spines.itervalues():
        spine.set_visible(False)


def figimage(img, scale=1, dpi=None):
    """Return figure and axes with figure tightly surrounding image.

    Unlike pyplot.figimage, this actually plots onto an axes object, which
    fills the figure. Plotting the image onto an axes allows for subsequent
    overlays.

    Parameters
    ----------
    img : array
        image to plot
    scale : float
        If scale is 1, the figure and axes have the same dimension as the
        image.  Smaller values of `scale` will shrink the figure.
    dpi : int
        Dots per inch for figure. If None, use the default rcParam.
    """
    dpi = dpi if dpi is not None else plt.rcParams['figure.dpi']

    h, w = img.shape
    figsize = np.array((w, h), dtype=float) / dpi * scale

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

    ax.set_axis_off()
    ax.imshow(img)
    return fig, ax


def cross_spines(zero_cross=False, ax=None):
    """Remove top and right spines from an axes.

    Parameters
    ----------
    zero_cross : bool
        If True, the spines are set so that they cross at zero.
    ax : :class:`~matplotlib.axes.Axes`
        Axes to modify. If None, use current axes.
    """
    ax = ax if ax is not None else plt.gca()

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    if zero_cross:
        ax.spines['bottom'].set_position('zero')
        ax.spines['left'].set_position('zero')
    return ax


def pad_limits(pad_frac=0.05, ax=None):
    """Pad data limits to nicely accomodate data.

    Padding is useful when you use markers, which often get cropped by tight
    data limits since only their center-positions are used to calculate limits.

    Parameters
    ----------
    pad_frac : float
        Padding is calculated as a fraction of the data span. `pad_frac = 0`
        is equivalent to calling plt.axis('tight').
    ax : :class:`~matplotlib.axes.Axes`
        Axes to modify. If None, use current axes.
    """
    ax = ax if ax is not None else plt.gca()
    ax.set_xlim(_calc_limits(ax.xaxis, pad_frac))
    ax.set_ylim(_calc_limits(ax.yaxis, pad_frac))


def _calc_limits(axis, frac):
    limits = axis.get_data_interval()
    if axis.get_scale() == 'log':
        log_limits = np.log10(limits)
        mag = np.diff(log_limits)[0]
        pad = np.array([-mag*frac, mag*frac])
        return 10**(log_limits + pad)
    elif axis.get_scale() == 'linear':
        mag = np.diff(limits)[0]
        pad = np.array([-mag*frac, mag*frac])
        return limits + pad


if __name__ == '__main__':
    from yutils.mpl.core import demo_plot

    f, ax = plt.subplots()
    demo_plot(ax)
    cross_spines(ax)
    ax.set_title('cross_spines')

    f, ax = plt.subplots()
    demo_plot(ax)
    pad_limits(ax=ax)
    ax.set_title('floating_yaxis with pad_limits')

    plt.show()

