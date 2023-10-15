import logging
import pathlib

import matplotlib
import matplotlib.pyplot as plt
import seaborn
import numpy as np
import pandas as pd

seaborn.set_style("whitegrid")
# seaborn.set_theme()

plt.rcParams['figure.figsize'] = [16.0, 7.0]  # [4, 2], [4, 3]
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

plt.rcParams['figure.dpi'] = 147


logger = logging.getLogger(__name__)


def savefig(fig, name, folder: pathlib.Path = '.',
            pdf=True,
            dpi=300  # default 'figure'
            ):
    """Save matplotlib Figure (having method `savefig`) as pdf and png."""
    folder = pathlib.Path(folder)
    fname = folder / name
    folder = fname.parent  # in case name specifies folders
    folder.mkdir(exist_ok=True, parents=True)
    fig.tight_layout()
    fig.savefig(fname.with_suffix('.png'), dpi=dpi)
    if pdf:
        fig.savefig(fname.with_suffix('.pdf'), dpi=dpi)
    logger.info(f"Saved Figures to {fname}")


def make_large_descriptors(size='xx-large'):
    """Helper function to have very large titles, labes and tick texts for
    matplotlib plots per default.

    size: str
        fontsize or allowed category. Change default if necessary, default 'xx-large'
    """
    plt.rcParams.update({k: size for k in ['xtick.labelsize',
                                           'ytick.labelsize',
                                           'axes.titlesize',
                                           'axes.labelsize',
                                           'legend.fontsize',
                                           'legend.title_fontsize']
                         })


def add_prop_as_second_yaxis(ax: matplotlib.axes.Axes, n_samples: int,
                             format_str: str = '{x:,.3f}') -> matplotlib.axes.Axes:
    """Add proportion as second axis. Try to align cleverly

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes for which you want to add a second y-axis
    n_samples : int
        Number of total samples (to normalize against)

    Returns
    -------
    matplotlib.axes.Axes
        Second layover twin Axes with right-hand side y-axis
    """
    ax2 = ax.twinx()
    n_min, n_max = np.round(ax.get_ybound())
    logger.info(f"{n_min = }, {n_max = }")
    lower_prop = n_min / n_samples + (ax.get_ybound()[0] - n_min) / n_samples
    upper_prop = n_max / n_samples + (ax.get_ybound()[1] - n_max) / n_samples
    logger.info(f'{lower_prop = }, {upper_prop = }')
    ax2.set_ybound(lower_prop, upper_prop)
    _ = ax2.set_yticks(ax.get_yticks()[1:-1] / n_samples)
    ax2.yaxis.set_major_formatter(
        matplotlib.ticker.StrMethodFormatter(format_str))
    return ax2


def format_large_numbers(ax: matplotlib.axes.Axes,
                         format_str: str = '{x:,.0f}') -> matplotlib.axes.Axes:
    """Format large integer numbers to be read more easily.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes which labels should be manipulated.
    format_str : str, optional
        Default float format string, by default '{x:,.0f}'

    Returns
    -------
    matplotlib.axes.Axes
        _description_
    """
    ax.xaxis.set_major_formatter(
        matplotlib.ticker.StrMethodFormatter(format_str))
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.StrMethodFormatter(format_str))
    return ax


def plot_feat_counts(df_counts: pd.DataFrame, feat_name: str, n_samples: int,
                     ax=None, figsize=(15, 10),
                     count_col='counts',
                     **kwargs):
    args = dict(
        ylabel='count',
        xlabel=f'{feat_name} ordered by completeness',
        title=f'Count and proportion of {len(df_counts):,d} {feat_name}s over {n_samples:,d} samples',
    )
    args.update(kwargs)

    ax = df_counts[count_col].plot(
        figsize=figsize,

        grid=True,
        ax=ax,
        **args)

    # default nearly okay, but rather customize to see minimal and maxium proportion
    # ax = peptide_counts['proportion'].plot(secondary_y=True, style='b')

    ax2 = add_prop_as_second_yaxis(ax=ax, n_samples=n_samples)
    ax2.set_ylabel('proportion')
    ax = format_large_numbers(ax=ax)
    return ax
