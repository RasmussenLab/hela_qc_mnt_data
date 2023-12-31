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
# # Analyse peptides
#
# ## Specification
# - access different levels of peptides easily
# - select training data per gene easily
#

# %%
import hela_data
from hela_data.transform import log
from config import PROTEIN_DUMPS
from hela_data.pandas import combine_value_counts
from matplotlib import table
import matplotlib.pyplot as plt
from config import FN_PROTEIN_SUPPORT_MAP, FN_PROTEIN_SUPPORT_FREQ
from tqdm.notebook import tqdm
import pickle
from config import KEY_FASTA_HEADER, KEY_FASTA_SEQ, KEY_PEPTIDES, KEY_GENE_NAME_FASTA
import ipywidgets as w
from collections import defaultdict
from config import FN_FASTA_DB, FN_ID_MAP, FN_PEPTIDE_INTENSITIES, FN_PEPTIDE_STUMP, FOLDER_DATA
from config import erda_dumps
import os
import time
import json
import logging

import pandas as pd
from IPython.core.debugger import set_trace


pd.options.display.float_format = '{:,.1f}'.format


logging.basicConfig(level=logging.INFO)  # configures root logger
logger = logging.getLogger()
logger.info("test")

# %%
id_map = pd.read_json(FN_ID_MAP, orient="split")

mask_no_gene = id_map.gene.isna()
id_map.loc[mask_no_gene, "gene"] = "-"

with open(FN_FASTA_DB) as f:
    data_fasta = json.load(f)

# %%
peptides_intensities = pd.read_pickle(erda_dumps.FN_PEPTIDES)
peptides_intensities.shape

# %%
# idx = peptides_intensities.index.levels[0][:1000]
peptides_intensities.head()

# %%
peptides_intensities = peptides_intensities.unstack()
peptides_intensities.head()


# %%
data_peptides = peptides_intensities
set(data_peptides.dtypes)

# %%
set_peptides = set(data_peptides.columns)

# %% [markdown]
# - switch between list of proteins with any support and non
#     - set threshold of number of peptides per protein over all samples (some peptides uniquely matched to one protein in on sample is just noise -> check razor peptides)
# - show support

# %%
peptides_2 = ('TTGIVMDSGDGVTHTVPIYEGYALPHAILRLDLAGR',
              'LDLAGRDLTDYLMK')

peptides_4 = ("ILTERGYSFTTTAEREIVR",
              "GYSFTTTAEREIVRDIK",
              "EIVRDIKEK",
              "DIKEKLCYVALDFEQEMATAASSSSLEK")
peptides_4[:0:-1]

# %%
# logger.setLevel(logging.DEBUG)
COLORS = ["\033[32;2m", "\033[32;1m", "0;34;47m"]


def annotate_overlap(peptides):
    i = len(peptides)
    if i > 3:
        raise ValueError("Two many peptides provided.")
    logging.debug(f"First peptide: {peptides[0]} ")
    base_peptide = peptides[0][::-1]
    logging.debug(f"Reversed pep:  {base_peptide}")
    colored_part = ""
    overlaps = []
    logging.debug(peptides[:0:-1])
    for pep in peptides[:0:-1]:

        logger.debug(f"Find overlap for: {pep}")
        overlap = ""
        overlap_in_last_step = False
        for j, amino_acid in enumerate(pep):
            overlap += amino_acid
            if overlap[::-1] != base_peptide[:len(overlap)]:
                overlap_now = False
            else:
                overlap_in_last_step = True
                logger.debug(f"Found overlap: {overlap}")
            if overlap_in_last_step and not overlap_now:
                overlaps.append(overlap)
                break
        logger.debug(
            f"Search remaining peptide: {base_peptide[len(overlap)::]}")
        base_peptide = base_peptide[len(overlap)::]
    overlaps.append(base_peptide[::-1])
    return overlaps[::-1]


assert ''.join(annotate_overlap(peptides_2)
               ) == "TTGIVMDSGDGVTHTVPIYEGYALPHAILRLDLAGR"
# annotate_overlap(peptides_4) # should raise ValueError
assert ''.join(annotate_overlap(peptides_4[0:3])) == 'ILTERGYSFTTTAEREIVR'
assert ''.join(annotate_overlap(peptides_4[1:])) == 'GYSFTTTAEREIVRDIK'

# %%
pep_0missed = "GYSFTTTAER"
pep_1missed = ["ILTERGYSFTTTAER",
               "GYSFTTTAEREIVR"]

# %%


pd.options.display.float_format = '{:,.1f}'.format

TGREEN = "\033[32;2m"  # Green Text
TGREEN_2 = "\033[32;1m"  # Green Text
RESET = "\033[0;0m"

w_first_letter = w.Dropdown(
    options=id_map[KEY_GENE_NAME_FASTA].str[0].unique())

w_genes = w.Dropdown(
    options=id_map.gene.loc[id_map[KEY_GENE_NAME_FASTA].str[0]
                            == w_first_letter.value].unique(),
    value='ACTB'
)

mask = id_map.gene == w_genes.value
selected = id_map.loc[mask, "protein"]


w_proteins_ids = w.Dropdown(options=selected.index)
w_protein = w.Dropdown(options=selected.unique())


def update_gene_list(first_letter):
    """Update proteins when new gene is selected"""
    mask_selected_genes = id_map[KEY_GENE_NAME_FASTA].str[0] == w_first_letter.value
    w_genes.options = id_map[KEY_GENE_NAME_FASTA].loc[mask_selected_genes].unique(
    )


_ = w.interactive_output(update_gene_list, {"first_letter": w_first_letter})


def update_protein_list(gene):
    mask = id_map[KEY_GENE_NAME_FASTA] == gene
    selected = id_map.loc[mask, "protein"]
    w_protein.options = selected.unique()
#     w_proteins_ids.options = selected.loc[selected == w_protein.value].index


_ = w.interactive_output(update_protein_list, {"gene": w_genes})


def update_protein_id_list(protein):
    """Update isotope list when protein is selected"""
    mask = id_map.protein == w_protein.value
    selected = id_map.protein.loc[mask]
    w_proteins_ids.options = selected.index


_ = w.interactive_output(update_protein_id_list, {'protein': w_protein})

d_peptides_observed_prot_id = defaultdict(list)


def show_sequences(prot_id):
    _data = data_fasta[prot_id]
    print(f"Protein_ID on Uniport: {prot_id}")
    print(f"HEADER: {_data[KEY_FASTA_HEADER]}")
#     print(f"Seq  : {_data[KEY_FASTA_SEQ]}")
    annotate_seq = "Peptides: "
    global d_peptides_observed_prot_id
    for i, _l in enumerate(_data[KEY_PEPTIDES]):
        annotate_seq += f"\nNo. of missed K or R: {i}"
        prot_seq_annotated = _data[KEY_FASTA_SEQ]
        _change_color = False
        for j, _pep in enumerate(_l):
            if _pep in set_peptides:
                d_peptides_observed_prot_id[prot_id].append(_pep)
                if _change_color is False:
                    _pep_in_green = TGREEN + f"{_pep}" + RESET
                    _change_color = True
                else:
                    _pep_in_green = TGREEN_2 + f"{_pep}" + RESET
                    _change_color = False
                prot_seq_annotated = prot_seq_annotated.replace(
                    _pep, _pep_in_green)
                _pep = _pep_in_green
            else:
                _change_color = False
            if j == 0:
                annotate_seq += "\n\t"
            else:
                annotate_seq += ",\n\t"
            annotate_seq += _pep

        print(f"Seq {i}: {prot_seq_annotated}")
    print(annotate_seq)

    _ = data_peptides[d_peptides_observed_prot_id[prot_id]].dropna(how='all')
    if _.columns.size > 2:
        display(_)
        display(_.describe())
    else:
        print("\nNo empirical evidence for protein")


w_out = w.interactive_output(show_sequences, {"prot_id": w_proteins_ids})

label_first_letter = w.Label(value='First letter of Gene')
label_genes = w.Label('Gene')
label_protein = w.Label('Protein')
label_proteins_ids = w.Label('Protein Isotopes')

panel_levels = w.VBox([
    w.HBox([
        w.VBox([label_first_letter, w_first_letter]),
        w.VBox([label_genes, w_genes]),
        w.VBox([label_protein, w_protein]),
        w.VBox([label_proteins_ids, w_proteins_ids])
    ]),
    w_out]
)
panel_levels

# %% [markdown]
# > create styler object?
#
# - [ ] replace zeros with NaN
# - [ ] display summary statistics on log-scale (but do not compute summary based on log-scale)

# %% [markdown]
# Get meta-data

# %%
query_template = "https://www.uniprot.org/uniprot/?query=accession:{prot_id}&format=txt"

# %% [markdown]
# - relatively short peptides resulting from one missed cleaveage, do not appear in the upper part.

# %% [markdown]
# - `gene` `->` `Protein_ID` (contains information of `gene` `->` `protein_isotopes`
# - `protein_ID` `->` `sequences` (`FN_FASTA_DB`)

# %%
# from hela_data.utils import sample_iterable

try:
    if (time.time() - os.path.getmtime(FN_PROTEIN_SUPPORT_MAP)) / 3600 / 24 > 7:
        # recompute file every week
        raise FileNotFoundError
    df_protein_support = pd.read_pickle(FN_PROTEIN_SUPPORT_MAP)
    with open(FN_PROTEIN_SUPPORT_FREQ, 'rb') as f:
        d_protein_support_freq = pickle.load(f)
except FileNotFoundError:
    d_protein_support = {}
    d_protein_support_freq = {}
    for prot_id in tqdm(data_fasta.keys()):
        _data = data_fasta[prot_id]
        peptides_measured = []
        for i, _l in enumerate(_data[KEY_PEPTIDES]):
            for _pep in _l:
                if _pep in set_peptides:
                    peptides_measured.append(_pep)
        _d_protein_support = {}
        _df_support_protein = data_peptides[peptides_measured].dropna(
            how='all')

        _n_samples = len(_df_support_protein)
        if _n_samples > 0:
            _d_protein_support['N_samples'] = _n_samples
            d_protein_support_freq[prot_id] = _df_support_protein.notna(
            ).sum().to_dict()
            d_protein_support[prot_id] = _d_protein_support
        else:
            d_protein_support[prot_id] = None

    df_protein_support = pd.DataFrame(d_protein_support).T.dropna()
    df_protein_support = df_protein_support.join(id_map)
    df_protein_support.to_pickle(FN_PROTEIN_SUPPORT_MAP)

    with open(FN_PROTEIN_SUPPORT_FREQ, 'wb') as f:
        pickle.dump(d_protein_support_freq, f)

# %%
l_proteins_good_support = df_protein_support.sort_values(
    by='N_samples').tail(100).index.to_list()

# %%
d_protein_support_freq['I3L3I0']

# %% [markdown]
# ## Connect to experimental peptide data
#
# Check if counts by `data_fasta`.

# %%

counts_observed_by_missed_cleavages = {}
for _protein_id, _data in tqdm(data_fasta.items()):
    _peptides = _data[KEY_PEPTIDES]
    _counts = {}
    for i, _l in enumerate(_peptides):
        _counts[i] = 0
        for _pep in _l:
            if _pep in set_peptides:
                _counts[i] += 1
    counts_observed_by_missed_cleavages[_protein_id] = _counts

# %%
df_counts_observed_by_missed_cleavages = pd.DataFrame(
    counts_observed_by_missed_cleavages
).T

# %%

fig, axes = plt.subplots(ncols=2, gridspec_kw={"width_ratios": [
                         5, 1], "wspace": 0.2}, figsize=(10, 4))

_counts_summed = df_counts_observed_by_missed_cleavages.sum()
_counts_summed.name = "frequency"

ax = axes[0]
_ = _counts_summed.plot(kind="bar", ax=ax)
ax.set_xlabel("peptides from n miscleavages")
ax.set_ylabel("frequency")

ax = axes[1]
ax.axis("off")
_ = pd.plotting.table(ax=ax, data=_counts_summed,
                      loc="best", colWidths=[1], edges='open')
_ = fig.suptitle('Peptides frequencies')

# %% [markdown]
# These are unnormalized counts in the meaning of that _razor_ peptides are counted as often as they are matched.

# %%
mask = df_counts_observed_by_missed_cleavages != 0
df_prot_observed = df_counts_observed_by_missed_cleavages.replace(0, pd.NA)

# %%
df_prot_observed = df_prot_observed.dropna(axis=0, how="all")
df_prot_observed = df_prot_observed.fillna(0)
df_prot_observed = df_prot_observed.convert_dtypes()

# %%

combine_value_counts(df_prot_observed)

# %%
freq_pep_mapped_to_protID = df_prot_observed.sum(axis=1).value_counts()
freq_pep_mapped_to_protID = freq_pep_mapped_to_protID.sort_index()

# %%
freq_pep_mapped_to_protID

# %% [markdown]
# ### Genes with support in data
#
# try software to identify the _most likely_ protein.
# [PyOpenMS](https://pyopenms.readthedocs.io/en/latest/) or
# [Pyteomics](https://pyteomics.readthedocs.io/en/latest/)?

# %%

# %% [markdown]
# ## Imputation: Train model
#
# > Select Gene or Protein
#
# As the samples are all obtained from the same biological sample (in principal), the single run should somehow be comparable.
# An description of variablity (from the Data Scientist perspective) can highlight some commenly known facts about proteomics experiments:
#  - batch effects: Measurements on consecutive days are have to be normalized to each other
#  - scoring: PSM are assigned to a peptide based on a score. Small variations can lead to different assignments
#
# Can a complex representation of a sample level out experimental variation on an in principle comparable data.
#
# ### Strategy
# - first start using peptides from single Protein_IDs
# - then move to all models from genes
# - explore structure

# %%
d_peptides_observed_prot_id

# %%
data_peptides.shape

# %%
w_select_proteins_good_support = w.Dropdown(options=l_proteins_good_support)
w_select_proteins_queried = w.Dropdown(
    options=list(d_peptides_observed_prot_id.keys()))

# select from top100 or above


def main_trigger(prot_id):
    """Explore protein data

    Global Variables used
    ---------------------
    data_peptides : pandas.DataFrame
    id_map : pandas.DataFrame
    d_peptides_observed_prot_id: dict


    Global variables set
    --------------------
    peptides_selected_log10: pandas.DataFrame
        Current selection of data for protein_id. All possible features are returned. log10 transformed
    prod_id : str
        Passed prot_id to function exposed globally
    """
    print(f'Protein Identifier: {prot_id}')
    # Select gene name, based on selected FASTA-File
    _gene_name = id_map.loc[prot_id, KEY_GENE_NAME_FASTA]
    # Protein Name summarized several UNIPROT isotopes (PROT, PROT_2, PROT_3, etc)
    _protein = id_map.protein.loc[prot_id]
    print(f'Gene Identifier {_gene_name}')
    # configure viewer above
    w_first_letter.value = _gene_name[0]
    w_genes.value = _gene_name
    w_protein.value = _protein
    w_proteins_ids.value = prot_id

    # get observed peptides according to pre-computed dictionary
    peptides_measured = d_peptides_observed_prot_id[prot_id]
    n_peptides_in_selection = len(peptides_measured)
    print(
        f"Found {n_peptides_in_selection} peptides measured of this protein.\n\n")

    # select subsample (as view) of peptides
    peptides_selected = data_peptides[peptides_measured]
    mask_selected_notna = data_peptides[peptides_measured].notna()
    selected_notna_summed_ax1 = mask_selected_notna.sum(axis=1)
    print("How many samples have how many peptides quantified?")
    for n_peptides, n_samples in selected_notna_summed_ax1.value_counts().sort_index().tail(10).items():
        print(f"In {n_samples:5} samples are {n_peptides:5} peptides measured.")

    PROP_DATA_COMPLETENESS = 0.5
    mask_samples_selected = selected_notna_summed_ax1 >= int(
        n_peptides_in_selection * PROP_DATA_COMPLETENESS)
    print(f"\nUsing a share of at least {PROP_DATA_COMPLETENESS}, "
          f"i.e. at least {int(n_peptides_in_selection * PROP_DATA_COMPLETENESS)} out of {n_peptides_in_selection}.",
          f"In total {mask_samples_selected.sum()} samples are selected for further analysis.", sep="\n")
    # from IPython.core.debugger import set_trace; set_trace()
    _ = peptides_selected.loc[mask_samples_selected, peptides_measured]
    _.index.name = f"protein_id {prot_id}"
    # _.to_json(PROTEIN_DUMPS / f"{prot_id}.json")

    display(_)
    # display(_.describe())
    global peptides_selected_log10
    peptides_selected_log10 = _.apply(log)  # selected in widget overview above
    display(peptides_selected_log10)
    display(peptides_selected_log10.describe())
    global prot_last
    prot_last = prot_id


w.VBox([
    w.HBox(
        [
            w.VBox(
                [
                    w.Label(
                        f"Top {len(l_proteins_good_support)} covered proteins"),
                    w_select_proteins_good_support,
                ]
            ),
            w.VBox([w.Label("Queried proteins from above"),
                   w_select_proteins_queried]),
        ]
    ),
    w.interactive_output(
        main_trigger, {"prot_id": w_select_proteins_good_support})
])

# %% [markdown]
# Idea: Select a protein which leads to training. Each selection will
# create a dump of the selected data, which can be used in the `XZY.ipynb`
# for model fine-tuning. ( A model per protein/gene?)

# %%
