# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown] Collapsed="false"
# # MaxQuant (MQ) Output-Files
#
# Compare a single experiment
#
# Files compared:
# 1. `Summary.txt`
# 2. `mqpar.xml`
# 3. `peptides.txt`
# 4. `proteins.txt`
#
# There is are many files more, where several files seem to be available in several times in different formats.

# %%
import os
import yaml
import logging
from pathlib import Path

from tqdm.notebook import tqdm

import pandas as pd
import ipywidgets as widgets

from hela_data.io.mq import MaxQuantOutputDynamic


from hela_data.file_utils import load_mqpar_xml
from hela_data.log import setup_logger_w_file

##################
##### CONFIG #####
##################
from config import FOLDER_MQ_TXT_DATA, FOLDER_PROCESSED
from config import FOLDER_KEY  # defines how filenames are parsed for use as indices

from config import FOLDER_DATA  # project folder for storing the data
print(f"Search MQ-Text-Files on path: {FOLDER_MQ_TXT_DATA}")

##################
### Logging ######
##################


ELIGABLE_FILE_PATHS = 'config/file_paths.yaml'

# Delete Jupyter notebook root logger handler
root_logger = logging.getLogger()
root_logger.handlers = []

logger = logging.getLogger('hela_data')
logger = setup_logger_w_file(logger, fname_base='log_00_maxquant_file_reader')

logger.info('Start with handlers: \n' + "\n".join(f"- {repr(log_)}" for log_ in logger.handlers))

# %%
with open(ELIGABLE_FILE_PATHS) as f:
    folders_dict = yaml.safe_load(f)

# %% Collapsed="false"
w_file = widgets.Dropdown(options=folders_dict, description='View files')
w_file

# %%
mq_output = MaxQuantOutputDynamic(w_file.value)
mq_output

# %% [markdown]
# Results will be saved in a subfolder under `hela_data/project/data` using the
# name of the specified input-folder per default. Change to your liking:

# %% [markdown]
# > Go to the block you are interested in!

# %% [markdown] Collapsed="false"
# ## MQ Summary files

# %%
mq_output.summary.iloc[0].to_dict()

# %% [markdown] Collapsed="false"
# ### File Handler
#
# - dictionary of run name to run output folder
# - find class with expected output folders

# %% [markdown] Collapsed="false"
# ### Summaries
#
# - aggregated in `hela_data/project/erda_05_parse_parameter_files.ipynb`
#     - file selection based on summaries for further analysis thereafter

# %% [markdown]
# - SIL - MS2 based on precursor which was a set of peaks
# - PEAK - MS2 scan based on a single peak on precursor spectrum
# - ISO - isotopic pattern detection
#

# %% [markdown] Collapsed="false"
# ## MaxQuant Parameter File
#
# - partly in a separate subfolder
# - mainly in run folders
# - rebase on folders_dictionary (check for `.xml` files in all folders)

# %%
mqpar_files = (Path(FOLDER_MQ_TXT_DATA.parent) / 'mqpar_files')

mqpar_files = [file for file in mqpar_files.iterdir() if file.suffix == '.xml']
len(mqpar_files)  # nested search needed

# %% Collapsed="false"
w_file = widgets.Dropdown(options=mqpar_files, description='Select a file')
w_file

# %% [markdown] Collapsed="false"
# ### Parameter Files

# %% Collapsed="false"
fname_mqpar_xml = os.path.join(FOLDER_PROCESSED, 'peptide_intensities.{}')

d_mqpar = dict()
for file in tqdm(mqpar_files):
    d_mqpar[file.stem] = load_mqpar_xml(file)['MaxQuantParams']

df_mqpar = pd.DataFrame(d_mqpar.values(), index=d_mqpar.keys()).convert_dtypes()
df_mqpar

# %% [markdown]
# The number of threads used might differ

# %%
df_mqpar['numThreads'].value_counts()

# %% [markdown]
# The parameter files would need further parsing, which is skipped for now:
#  - `OrderedDict` would need to be flattend
#  - in the example below, it is not easy to see how entries should be easily combined
#     (list of `OrderedDict`s where only the `fastaFilePath` is different)

# %%
df_mqpar.iloc[0].loc['fastaFiles']

# %% [markdown]
# in order to see if there are different setting based on the string columns, drop duplicates
#
# - only one should remain

# %%
df_mqpar.select_dtypes('string').drop('numThreads', axis=1).drop_duplicates()

# %% [markdown] Collapsed="false"
# ## Peptides
#
# - peptides combined (combining different charged states): `peptides`
# - single peptides (with differing charges): `evidence`

# %% Collapsed="false"
pd.set_option('display.max_columns', 60)

# mq_output = MaxQuantOutputDynamic(
#     folder=folders[random.randint(0, len(paths_peptides.files)-1)])
mq_output.peptides

# %%
mq_output.evidence

# %%
mq_output.peptides.Intensity  # as is in peptides.txt, comma seperated thousands

# %% [markdown] Collapsed="false"
# ## Theoretial Peptides from used fasta-file
#
# > `misc_FASTA_tryptic_digest.ipynb`
#
# - check if peptides are part of theoretical peptides

# %% Collapsed="false"
