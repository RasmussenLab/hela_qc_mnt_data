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
# # MaxQuantOutput

# %%
import pandas as pd
from pathlib import Path
import ipywidgets as w

import hela_data.io as io
import hela_data.io.mq as mq

from config import FOLDER_MQ_TXT_DATA

folders = io.search_subfolders(path=FOLDER_MQ_TXT_DATA, depth=1, exclude_root=True)
w_folder = w.Dropdown(options=folders, description='Select a folder')
w_folder

# %% [markdown]
# ## MaxQuantOutput class
#
# Instead of handling the files manually in a MQ folder, e.g. like

# %%
all_files = io.search_files(path=w_folder.value, query='')
all_files

# %% [markdown]
# files can just be accessed using the `MaxQuantOutput` class.

# %%
mq_output = mq.MaxQuantOutput(w_folder.value)
mq_output

# %% [markdown]
# This lists the files in the current folder for you (calling `search_files`):

# %%
mq_output.files

# %% [markdown]
# And extends the class attributes on intialization by the expected files (statically):

# %%
mq_output._inital_attritubutes

# %%
mq_output.get_list_of_attributes()

# %%
# not able to delete yet. __getitem__ better alternative?
# lookup
# del mq_output.OxidationMSites

# %%
{Path(x).stem: x for x in mq_output.files}

# %%
# mq_output.evidence(mq_output)
mq_output.peptides

# %% [markdown]
# ### Dynamic Attribute lookup
#
# try to use `__getattr__`, maybe `__setattr__`?
#
# This version offers less inspection possibilities as the attributes are only set when they are looked up.

# %%
mq_output = mq.MaxQuantOutputDynamic(w_folder.value)
mq_output

# %%
mq_output.file_keys

# %%
mq_output.peptides

# %%
try:
    mq_output.peptides_
except AttributeError as e:
    print(*e.args)

# %%
mq_output.get_list_of_attributes()

# %% [markdown]
# ## Files

# %% [markdown]
# ### evidence.txt
#
# > some columns throw a warning

# %%
pd.options.display.max_columns = len(mq_output.evidence.columns)
mq_output.evidence.head()

# %%
mixed_dtype_columns = mq_output.evidence.columns[[50, 53, 58]]
mq_output.evidence[mixed_dtype_columns][mixed_dtype_columns[1]]

# %%
