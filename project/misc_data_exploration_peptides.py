# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: hela_data
#     language: python
#     name: hela_data
# ---

# %% [markdown]
# # Peptides

# %%
from random import sample
import ipywidgets as w
from hela_data.plotting import savefig
from datetime import datetime
import ipywidgets as widgets
from functools import partial
import config
from config import erda_dumps
from hela_data.analyzers import analyzers

# %%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# %%
pd.options.display.max_columns = 100
pd.options.display.min_rows = 30

# %% [markdown]
# Data file and other configurations:
#
# - [ ] file reader for peptide intensities

# %%
# FN_PEPTIDE_INTENSITIES = config.FOLDER_DATA / 'df_intensities_N07813_M01000'
# analysis = analyzers.AnalyzePeptides.from_csv(FN_PEPTIDE_INTENSITIES, index_col=0)
# INDEX_NAME = 'Sample ID'
# analysis.df.index.name = INDEX_NAME

# config.FOLDER_DATA / 'df_intensities_peptides_wide_2017_2018_2019_2020_N05011_M42725.pkl'
FN_PEPTIDE_INTENSITIES = erda_dumps.FN_PEPTIDES
analysis = analyzers.AnalyzePeptides.from_pickle(FN_PEPTIDE_INTENSITIES)

peptides = analysis.df


# %%
analysis.df.iloc[:10, :10]

# %%
X = analysis.df

# %%
N_MIN_OBS = 10
mask_min_obsevation = X.notna().sum() >= N_MIN_OBS
mask_min_obsevation.sum()

# %% [markdown]
# ## Cleaning step
#
# - remove fractionated samples (need to be re-run and added to the analysis)

# %%
queries = set()


def find_indices_containing_query(query):
    mask = X.index.str.contains(query)
    X_query = X.loc[mask].sort_index()
    queries.add(query)
    return X_query


# %%
X_frac = find_indices_containing_query('[Ff]rac')
X_frac.index


# %%
def get_unique_stub(X: pd.Index):
    # X_frac_unique = sorted(list(set())) # matches too much
    ret = X.str.split('frac').str[0].str.rsplit('_', n=1).str[0]
    return sorted(list(set(ret)))


X_frac_unique = get_unique_stub(X_frac.index)

# %%


def show_fractions(stub: str, df):
    subset = df[df.index.str.contains(stub)]
    display(subset)
    display(subset.notna().sum(axis=1))


w_data = widgets.Dropdown(options=X_frac_unique, index=0)

# show_fractions(stub=X_frac_unique[2], df=X_frac)

show_fractions = partial(show_fractions, df=X_frac)
out_sel = widgets.interactive_output(show_fractions, {'stub': w_data})
widgets.VBox([w_data, out_sel])

# %% [markdown]
# - check for file names with `exp`. Some seem to be fractionated samples

# %%
X_exp = find_indices_containing_query('_exp\\d_')
X_exp.index

# %%
assert find_indices_containing_query('[gG][pP][fF]').empty

# %%
find_indices_containing_query('[cC][vV]').index

# %% [markdown]
# remove singe fraction samples (need to be quantified as one)

# %%
X.drop(labels=X_frac.index, inplace=True)
X.drop(labels=X_exp.index, inplace=True)

# %%
# should be part of analysis
mask_less_than_500 = X.notna().sum(axis=1) < 500
print(X.loc[mask_less_than_500].sort_index().notna().sum(axis=1).to_string())  # 'samples_potentially_fractionated.txt'

# %%
['concat', 'HpH', 'ingel']


# %% [markdown]
# ## Peptitome is spares

# %%
def get_sorted_not_missing(X: pd.DataFrame):
    """Return a Dataframe with missing values. Order columns by degree of completness
    over columns from variables least to most shared among observations."""
    X = X.notna().astype(int)
    return X[X.mean().sort_values().index]


# %%
# %time not_missing = get_sorted_not_missing(X)
not_missing.iloc[:, -10:].describe()

# %%
not_missing.iloc[:10, -10:]

# %%
grid_kws = {"width_ratios": (.9, .05), "hspace": 0.5}
N_MOST_COMMON_PEPTIDES = 300
data_to_visualize = not_missing.iloc[:, -N_MOST_COMMON_PEPTIDES:]
print(f"Look at missingness pattern of {N_MOST_COMMON_PEPTIDES} most common peptides across sample.\n"
      f"Data matrix dimension used for printing: { data_to_visualize.shape}")

fig_heatmap_missing, (axes_heatmap_missing, cbar_ax) = plt.subplots(1, 2, gridspec_kw=grid_kws, figsize=(12, 8))
axes_heatmap_missing = sns.heatmap(data_to_visualize,
                                   ax=axes_heatmap_missing,
                                   cbar_ax=cbar_ax,
                                   cbar_kws={"orientation": "vertical"})


# %% [markdown]
# White patches indicates that a peptide has been measured, black means it was not measured. Some samples (rows) have few of the most common peptides. This suggests to set a minimum of total peptides in a sample, which is common pratice.
#
# > An algorithm should work with the most common peptides and base it's inference capabilities after training on these.

# %%
# # This currently crashes if you want to have a pdf
datetime_now = datetime.now()

savefig(fig_heatmap_missing, f'peptides_heatmap_missing_{datetime_now:%y%m%d}', folder=config.FIGUREFOLDER, pdf=False)

# %% [markdown]
# ## Sample stats

# %%
TYPE = 'peptides'
COL_NO_MISSING, COL_NO_IDENTIFIED = f'no_missing_{TYPE}', f'no_identified_{TYPE}'
COL_PROP_SAMPLES = 'prop_samples'


def compute_stats_missing(X):
    """Dataset of repeated samples indicating if an observation
    has the variables observed or missing x\\in\\{0,1\\}"""
    sample_stats = X.index.to_frame(index=False).reset_index()
    sample_stats.columns = ['SampleID_int', 'INDEX']
    sample_stats.set_index('INDEX', inplace=True)

    sample_stats[COL_NO_IDENTIFIED] = X.sum(axis=1)
    sample_stats[COL_NO_MISSING] = (X == 0).sum(axis=1)

    assert all(sample_stats[[COL_NO_IDENTIFIED, COL_NO_MISSING]].sum(axis=1) == X.shape[1])
    sample_stats = sample_stats.sort_values(by=COL_NO_IDENTIFIED, ascending=False)
    sample_stats[COL_PROP_SAMPLES] = np.array(range(1, len(sample_stats) + 1)) / len(sample_stats)
    return sample_stats


sample_stats = compute_stats_missing(not_missing)

# %%
sample_stats

# %%
fig_ident = sns.relplot(x='SampleID_int', y=COL_NO_IDENTIFIED, data=sample_stats)
fig_ident.set_axis_labels('Sample ID', f'Frequency of identified {TYPE}')
fig_ident.fig.suptitle(f'Frequency of identified {TYPE} by sample id', y=1.03)
savefig(fig_ident, f'identified_{TYPE}_by_sample', folder=config.FIGUREFOLDER)

fig_ident_dist = sns.relplot(x=COL_PROP_SAMPLES, y=COL_NO_IDENTIFIED, data=sample_stats)
fig_ident_dist.set_axis_labels('Proportion of samples (sorted by frequency)', f'Frequency of identified {TYPE}')
fig_ident_dist.fig.suptitle(f'Frequency of identified {TYPE} groups by sample id', y=1.03)
savefig(fig_ident_dist, f'identified_{TYPE}_ordered', folder=config.FIGUREFOLDER)

# %%
COL_NO_MISSING_PROP = COL_NO_MISSING + '_PROP'
sample_stats[COL_NO_MISSING_PROP] = sample_stats[COL_NO_MISSING] / float(X.shape[1])

# from ggplot import *
# ggplot(aes(x='nan_proc'), data = nonnan) + geom_histogram(binwidth = 0.005) #+ ylim(0,0.025)
sns.set(style="darkgrid")
g = sns.relplot(x='prop_samples', y=COL_NO_MISSING_PROP, data=sample_stats)
plt.subplots_adjust(top=0.9)
g.set_axis_labels("Proportion of samples (sorted by frequency)", "proportion missing")
g.fig.suptitle(f'Proportion of missing {TYPE} ordered')
savefig(g, "proportion_proteins_missing", folder=config.FIGUREFOLDER)


# %% [markdown]
# ## Look at sequences

# %%
class SequenceAnalyser():

    def __init__(self, sequences: pd.Series):
        if not isinstance(sequences, pd.Series):
            raise ValueError("Please provide a pandas.Series, not {}".format(type(sequences)))
        self.sequences = sequences

    def calc_counts(self, n_characters):
        return self.sequences.str[:n_characters].value_counts()

    def length(self):
        return self.sequences.str.len().sort_values()


# %%
sequences = SequenceAnalyser(analysis.df.columns.to_series())
sequences.length()

# %%
w.interact(sequences.calc_counts, n_characters=w.IntSlider(value=4, min=1, max=55))

# %%
sequences_p4 = sequences.calc_counts(4)
display(sequences_p4.head())
sequences_p4.loc[sequences_p4.isin(('CON_', 'REV_'))].sort_index()

# %% [markdown]
# What to do when
#
#
# ```
# AAAAAAAAAAGAAGGRGSGPGR
# AAAAAAAAAAGAAGGRGSGPGRR
#
# AAAANSGSSLPLFDCPTWAGKPPPGLHLDVVK
# AAAANSGSSLPLFDCPTWAGKPPPGLHLDVVKGDK
# ```
#
#

# %% [markdown]
# ## Select Proteins

# %% [markdown]
# ### Minumum required sample quality
# First define the minum requirement of a sample to be kept in

# %%
MIN_DEPTH_SAMPLE = int(X.shape[-1] * 0.25)
w_min_depth_sample = w.IntSlider(value=MIN_DEPTH_SAMPLE, min=0, max=max(sample_stats[COL_NO_IDENTIFIED]))
print(f'Minimum {TYPE} per sample observed:')
w_min_depth_sample

# %%
mask_samples = sample_stats[COL_NO_IDENTIFIED] >= w_min_depth_sample.value
print(f"Selected {mask_samples.sum()} samples")

# %% [markdown]
# ### Distribution of Intensity values
# - comparing non-transformed to $\log_{10}$ transformed

# %%
sample = X.sample(axis=0).iloc[0]
sample_id = sample.name  # int(sample_stats.loc[sample.index].SampleID_int)
print("Sample ID:", sample_id)
sns.set(style="darkgrid")
sample = sample.dropna()
fig, axes = plt.subplots(1, 2, figsize=(10, 3))
sns.distplot(sample, bins=100, ax=axes[0])
axes[0].set_title("Unnormalized distribution")

sample_log = np.log(sample)  # natural logarithm, could also be base_2, base_10 logarithm
sns.distplot(sample_log, bins=100, ax=axes[1])
axes[1].set_title('log (ln) normalized distribution')

_ = fig.suptitle(f"Dynamic Range of measured intensities in sample {sample_id}")
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
savefig(fig, 'distribution_peptides_sample_' + str(sample_id), folder=config.FIGUREFOLDER)

# %%
sample = X.sample(axis=1)
sample_id = sample.columns[0]
print("Sample ID:", sample_id)
sns.set(style="darkgrid")
sample = sample.dropna()
fig, axes = plt.subplots(1, 2, figsize=(10, 3))
sns.distplot(sample, bins=100, ax=axes[0])
axes[0].set_title("Unnormalized distribution")

sample_log = np.log2(sample)  # natural logarithm, could also be base_2, base_10 logarithm
sns.distplot(sample_log, bins=100, ax=axes[1])
axes[1].set_title('log (ln) normalized distribution')

fig.suptitle(f"Dynamic range of {sample_id} between samples")
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
savefig(fig, 'distribution_peptides_sample_' + str(sample_id), folder=config.FIGUREFOLDER)

# %% [markdown]
# ### Reference table intensities (natural logarithm)
#
# 14 to 23 spans a dynamic range of 3 orders of base 10

# %%
dynamic_range = pd.DataFrame(range(14, 24), columns=['x'])
dynamic_range['$e^x$'] = dynamic_range.x.apply(np.exp)
dynamic_range.set_index('x', inplace=True)
dynamic_range.index.name = ''
dynamic_range.T

# %% [markdown]
# ## Next UP

# %% [markdown]
# ### Find Protein of Peptides
# - check with some reference list of peptides: This is created in `project\FASTA_tryptic_digest.ipynb`
