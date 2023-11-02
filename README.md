# HeLa data quality control (QC) and maintenance (MNT) samples

We provide 7,444 samples through the PRIDE archiv (PX------). 

Publication:
> Webel, Henry, Yasset Perez-Riverol, Annelaura Bach Nielson, and Simon Rasmussen. 2023.
> “Mass Spectrometry-Based Proteomics Data from Thousands of HeLa Control Samples.”
> Research Square. https://doi.org/10.21203/rs.3.rs-3083547/v1.

The projocet folder contains notebooks for data processing of MaxQaunt text output folders
which were created using the **workflows**, processing each file separately.

## Project

The project folder contains notebooks for data processing of MaxQaunt text output folders
and the analysis of the data for the publication, see its [README](project/README.md) for details.

## Workflows

The workflows folder in the repository contains snakemake workflows used for rawfile data processing, 
both for running MaxQuant over a large set of HeLa raw files 
and ThermoRawFileParser on a list of raw files to extract their meta data.

### MaxQuant

Process single raw files using MaxQuant. See [README](workflows/maxquant/README.md) for details.

### Metadata

Read metadata from single raw files using MaxQuant. See [README](workflows/metadata/README.md) for details.


## Setup

create a new environment in case you want to have aseparate installations
```
conda create -n hela_data -c conda-forge -c defaults python numpy matplotlib pandas plotly seaborn fastcore omegaconf ipywidgets tqdm pyyaml umap-learn scikit-learn openpyxl xmltodict
# jupyterlab # maybe add a jupyterlab installation (depends on your setup)
conda activate hela_data
```

and then install the custom code (and dependencies, which should be installed already installed if you use the above environment):

```
pip install . # . for current directory which should be this repository
```

