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
# # Protein sequence aggregation by gene

# %%
from collections import defaultdict
import itertools
import json
from pprint import pprint
from tqdm.notebook import tqdm

import pandas as pd

try:
    from Bio import Align
except ImportError:
    # !pip install biopython
    from Bio import Align

from config import FN_FASTA_DB
from config import fasta_entry as fasta_keys

# %%
with open(FN_FASTA_DB) as f:
    data_fasta = json.load(f)  # , indent=4, sort_keys=False)
len(data_fasta)

# %%
gene_isotopes = defaultdict(list)
protein_wo_gene = []
for key, fasta_entry in tqdm(data_fasta.items()):
    gene = fasta_entry[fasta_keys.gene]
    if gene:
        gene_isotopes[gene].append(key)
    else:
        protein_wo_gene.append(key)

print(f"#{len(protein_wo_gene)} proteins have not gene associated: {', '.join(protein_wo_gene[:10])}, ...")

# %%
gene = 'ACTG1'  # Actin as a contaminant protein
gene_isotopes[gene]

# %%
for isotope in gene_isotopes[gene]:
    pprint(data_fasta[isotope])

# %% [markdown]
# ## Sequences

# %%
sequences = {}
for isotope in gene_isotopes[gene]:
    sequences[isotope] = data_fasta[isotope][fasta_keys.seq]
sequences

# %%
sorted(sequences.values(), key=len)

# %%
sequences = pd.Series(sequences)
sequences.str.len()

# %%
aligner = Align.PairwiseAligner()

# %%
# Identical? Maybe check if this is more than once the case?
alignments = aligner.align(sequences.loc['I3L1U9'], sequences.loc['I3L3I0'])
for alignment in alignments:
    print(alignment)

# %%
data_fasta['I3L1U9'][fasta_keys.seq] == data_fasta['I3L3I0'][fasta_keys.seq]

# %%
alignments = aligner.align(sequences.loc['I3L1U9'], sequences.loc['I3L3R2'])  # Identical?
for alignment in alignments:
    print(alignment)
    break

# %%
alignments = aligner.align(sequences.loc['P63261'], sequences.loc['K7EM38'])  # Identical?
for alignment in alignments:
    print(alignment)
    break

# %% [markdown]
# ## Unique Peptides

# %%
peptides = {}
for isotope in gene_isotopes[gene]:
    sequences[isotope] = data_fasta[isotope][fasta_keys.peptides][0]

for peptides in itertools.zip_longest(*sequences.values, fillvalue=''):
    if len(set(peptides)) == 1:
        print(f'all identical: {peptides[0]}')
    else:
        print('\t'.join(peptides))

# %%
for j, peptides in enumerate(sequences.values):
    if j == 0:
        set_overlap = set(peptides)
    else:
        set_overlap = set_overlap.intersection(peptides)
set_overlap

# %%
