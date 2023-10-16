# Project

The folder contains the notebooks used for transforming the MaxQuant output data (see workflow in root of repository) stored on a long term file storage system. The data
could be manipulated through a Jupyter Hub instance, and the execution was thus done through notebooks.
The rawfile metadata from the workflow extracting this information (see workflow in root of repository), was added. 

See the README's in `config` and `data` for minimum files which need to be present. The notebooks are mainly for documentation and 
re-execution for the authors, but applying it to other data, should possible with updates.

## Notebooks
- erda: Is the longterm storage of the university -> MaxQuant output was processed on a server attached to erda
- hela: dumps from erda processing (raw file names, aggregated `summaries.txt` from MQ, protein groups, peptides and precursor dumps)

tag | notebook  | Description
--- | ---  |  --- 
Development data related 
erda | erda_01_mq_select_runs.ipynb         | Aggregate current summary files from MQ runs into table
erda | erda_02_mq_count_features.ipynb      | Aggregate information from all eligable MQ runs <br> Saves processed files used for data selection (Counters used in `erda_03_training_data.ipynb`)
erda | erda_03_training_data.ipynb          | Build training data dump (run for each data level) in wide format
erda | erda_04_transpose_data.ipynb         | Transpose dataset (row: a sample), separate as erda has memory limits, dump counts and present-absent patterns
erda | erda_12_explore_raw_MQ_data.ipynb    | Load a single MQ txt output folder and browse data <br> dumps large pickle files for training
erda | erda_data_available.ipynb            | Plots on theoretically available data based on Counter dictionaries
hela | 00_0_hela_metadata_rawfiles.ipynb         |  Analyze rawfile metadata and prepare for data selection
hela | 00_1_hela_MQ_summaries.ipynb              | Analyzse summaries.txt data from all samples
hela | 00_2_hela_all_raw_files.ipynb             | Find duplicate raw files, analyze sizes
hela | 00_3_hela_selected_files_overview.ipynb   | Data description based on file size and metaddata of selected files
hela | 00_3_1_pride_metadata_analysis.ipynb      | **Analysis for Data Descriptor paper of uploaded metadata (Figure 2)** 
hela | 00_4_hela_development_dataset_splitting   | Splitting data into development datasets of HeLa cell line data (based on wide format input from `erda_03` and `erda_04`)
Single development dataset |
hela | 00_5_hela_development_dataset_support.ipynb    | Support of training data samples/feat on selected development data set
hela | 00_6_hela_training_data_exploration.ipynb  | Explore a data set for diagnositics <br>  Visualize key metrics
Miscancellous notebooks on different topics (partly exploration) |
misc | misc_data_exploration_peptides.ipynb | Describe current peptides training data
misc | misc_FASTA_data_agg_by_gene.ipynb    | Investigate possibility to join proteins by gene
misc | misc_FASTA_tryptic_digest.ipynb      | Analyze fasta file used for peptide identification
misc | misc_MaxQuantOutput.ipynb            | \[documentation\] Analyze MQ output, show MaxQuantOutput class behaviour
misc | misc_protein_support.ipynb           | peptide sequences mapped to protein sequences

# Description (tbc)

## erda notebooks

- [ ] determine order and rename accordingly with prefix

The data is for now processed only using MaxQuant. If the files are processed
by another Software, these notebooks need to be adapted for if they contain `mq` or `MQ`.

### erda_01_mq_select_runs

- read in all summaries and select eligable runs based on number of identified peptides

### erda_02_mq_count_features

- Feature Extraction and Feature counting
- dumps extracted features per group into `FOLDER_PROCESSED`
  (separated for type and by year)

### erda_03_training_data

- needs to be executed for each data type
- loads a python config file (setting `FeatureCounter` classes and custom functions)
  along string configuration variables

## HeLa notebooks - Training data


### `00_0_1_rawfile_renaming.ipynb`

> internal, documentation only (see pride upload for result)

- create a new id for each raw file based on the creation date and instrument
- uses metadata
- build lftp commands for pride upload

### `00_0_hela_metadata_rawfiles.ipynb`

- group by MS instrument parameters
- create `data/files_per_instrument_nested.yaml` for selection of data by massspectrometer

### `00_1_hela_MQ_summaries.ipynb`

- analysze all `summaries.txt`

### `00_2_hela_all_raw_files.ipynb`

### `00_3_hela_selected_files_overview.ipynb`

- created joined metadata file 
- overview of metadata of selected files for data descriptor paper

### `00_4_hela_development_dataset_splitting.ipynb`

- Create development dataset(s) of common machines, one for each machine
- UMAP **Figure 1b**, statistics of **Figure 1c**
- create datasets for training PIMMS models

### Training data inspection

### `00_5_hela_development_dataset_support.ipynb`

- feature counts for a single development dataset (e.g. for a single machine)

### `00_6_hela_training_data_exploration.ipynb`

> needs clean-up

- explore a data set for diagnositics
