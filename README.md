# HeLa data quality control (QC) and maintenance (MNT) samples

We provide 7,444 samples through the PRIDE archiv ([PXD042233](https://www.ebi.ac.uk/pride/archive/projects/PXD042233)). 

Publication:
> Webel, Henry, Yasset Perez-Riverol, Annelaura Bach Nielson, and Simon Rasmussen (2024):
> Mass spectrometry-based proteomics data from thousands of HeLa control samples. 
> Sci Data 11, 112 https://doi.org/10.1038/s41597-024-02922-z

The projocet folder contains notebooks for data processing of MaxQaunt text output folders
which were created using the **workflows**, processing each file separately.

## Curated dumps

We provide metadata from the raw files together with the MaxQuant summary statistics of 
analzying the raw files in `pride_metadata.csv`. You can read it in python using pandas
directly from the PRIDE [FTP folder of the project](https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233).

```python
import pandas as pd
pd.options.display.max_columns = 80

ftp_folder = 'https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233'
file = 'pride_metadata.csv'

df = pd.read_csv(f'{ftp_folder}/{file}', index_col=0)
df.sample(5, random_state=42).sort_index()
```
will yield

| Sample ID                                      | Pathname                                                                   |      bytes |   size_gb |   Version | Content Creation Date   | Thermo Scientific instrument model   | instrument attribute     | instrument serial number   | Software Version      | firmware version   |   Number of MS1 spectra |   Number of MS2 spectra |   MS min charge |   MS max charge |   MS min RT |   MS max RT |   MS min MZ |   MS max MZ |   scan start time |   mass resolution |   mass unit |   Number of scans | MS scan range   | Retention time range   | Mz range   | beam-type collision-induced dissociation   | sample number   | Vial   |   injection volume setting |   Row |   dilution factor |   Comment |   collision-induced dissociation |   sample name |   Type | Enzyme    | Enzyme mode   | Use enzyme first search   | Variable modifications                | Fixed modifications   | Use variable modifications first search   | Requantify   |   Multiplicity |   Max. missed cleavages | LC-MS run type   |    MS |   MS/MS |   MS3 |   MS/MS Submitted |   MS/MS Submitted (SIL) |   MS/MS Submitted (ISO) |   MS/MS Submitted (PEAK) |   MS/MS Identified |   MS/MS Identified (SIL) |   MS/MS Identified (ISO) |   MS/MS Identified (PEAK) |   MS/MS Identified [%] |   MS/MS Identified (SIL) [%] |   MS/MS Identified (ISO) [%] |   MS/MS Identified (PEAK) [%] |   Peptide Sequences Identified |   Peaks |   Peaks Sequenced |   Peaks Sequenced [%] |   Peaks Repeatedly Sequenced |   Peaks Repeatedly Sequenced [%] |   Isotope Patterns |   Isotope Patterns Sequenced |   Isotope Patterns Sequenced (z>1) |   Isotope Patterns Sequenced [%] |   Isotope Patterns Sequenced (z>1) [%] |   Isotope Patterns Repeatedly Sequenced |   Isotope Patterns Repeatedly Sequenced [%] | Recalibrated   |   Av. Absolute Mass Deviation [ppm] |   Mass Standard Deviation [ppm] |   Av. Absolute Mass Deviation [mDa] |   Mass Standard Deviation [mDa] |
|:-----------------------------------------------|:---------------------------------------------------------------------------|-----------:|----------:|----------:|:------------------------|:-------------------------------------|:-------------------------|:---------------------------|:----------------------|:-------------------|------------------------:|------------------------:|----------------:|----------------:|------------:|------------:|------------:|------------:|------------------:|------------------:|------------:|------------------:|:----------------|:-----------------------|:-----------|:-------------------------------------------|:----------------|:-------|---------------------------:|------:|------------------:|----------:|---------------------------------:|--------------:|-------:|:----------|:--------------|:--------------------------|:--------------------------------------|:----------------------|:------------------------------------------|:-------------|---------------:|------------------------:|:-----------------|------:|--------:|------:|------------------:|------------------------:|------------------------:|-------------------------:|-------------------:|-------------------------:|-------------------------:|--------------------------:|-----------------------:|-----------------------------:|-----------------------------:|------------------------------:|-------------------------------:|--------:|------------------:|----------------------:|-----------------------------:|---------------------------------:|-------------------:|-----------------------------:|-----------------------------------:|---------------------------------:|---------------------------------------:|----------------------------------------:|--------------------------------------------:|:---------------|------------------------------------:|--------------------------------:|------------------------------------:|--------------------------------:|
| 2016_01_15_15_17_Q-Exactive-HF-Orbitrap_148    | MNT_2016_Proteomics/2016_01_15_15_17_Q-Exactive-HF-Orbitrap_148.raw        | 1501447123 |   1.39833 |        66 | 2016-01-15 15:17:43     | Q Exactive HF Orbitrap               | Q Exactive HF Orbitrap   | Exactive Series slot #148  | 2.5-204201/2.5.0.2042 | rev. 1             |                   12920 |                   80807 |               2 |              19 |  0.00376826 |     144.005 |     300.147 |     1731.34 |        0.00376826 |               0.5 |         nan |             93727 | 1:93727         | 0.0037682586:144.00486 | 100:6000   | HCD                                        | nan             | A4     |                        5   |     4 |                 1 |       nan |                              nan |           nan |    nan | Trypsin/P | Specific      | False                     | Oxidation (M);Acetyl (Protein N-term) | Carbamidomethyl (C)   | False                                     | False        |              1 |                       2 | Standard         | 12920 |   80807 |     0 |             89679 |                   71935 |                       0 |                    17744 |              44494 |                    43025 |                        0 |                      1469 |                     50 |                           60 |                            0 |                           8.3 |                          34109 | 1288500 |             77301 |                   6   |                         1906 |                              2.5 |             197041 |                        67285 |                              66513 |                               34 |                                     38 |                                    4056 |                                         6   | +              |                             0.62615 |                         0.92066 |                             0.41545 |                         0.63975 |
| 2016_04_16_01_56_Q-Exactive-HF-Orbitrap_147    | MNT_2016_Proteomics/2016_04_16_01_56_Q-Exactive-HF-Orbitrap_147.raw        | 2464568579 |   2.29531 |        66 | 2016-04-16 01:56:38     | Q Exactive HF Orbitrap               | Q Exactive HF Orbitrap   | Exactive Series slot #147  | 2.5-204201/2.5.0.2042 | rev. 1             |                   12233 |                   87090 |               2 |               5 |  0.00228172 |     264.002 |     300.165 |     1730.02 |        0.00228172 |               0.5 |         nan |             99323 | 1:99323         | 0.0022817164:264.00169 | 50:6000    | HCD                                        | A1              | G12    |                        5   |   nan |                 1 |       nan |                              nan |           nan |    nan | Trypsin/P | Specific      | False                     | Oxidation (M);Acetyl (Protein N-term) | Carbamidomethyl (C)   | False                                     | False        |              1 |                       2 | Standard         | 12233 |   87090 |     0 |             89595 |                   84585 |                       0 |                     5010 |              54273 |                    53380 |                        0 |                       893 |                     61 |                           63 |                            0 |                          18   |                          35604 | 1818019 |             70726 |                   3.9 |                        13395 |                             19   |             272433 |                        65019 |                              64483 |                               24 |                                     26 |                                   15913 |                                        24   | +              |                             0.41731 |                         0.59783 |                             0.2454  |                         0.35516 |
| 2018_09_07_15_59_Q-Exactive-HF-X-Orbitrap_6011 | MNT_2018_Proteomics/2018_09_07_15_59_Q-Exactive-HF-X-Orbitrap_6011.raw     | 3097450763 |   2.88473 |        66 | 2018-09-07 15:59:23     | Q Exactive HF-X Orbitrap             | Q Exactive HF-X Orbitrap | Exactive Series slot #6011 | 2.9-290033/2.9.0.2923 | rev. 1             |                   13344 |                  118993 |               2 |              58 |  0.00364904 |     144.002 |     300.129 |     1657.28 |        0.00364904 |               0.5 |         nan |            132337 | 1:132337        | 0.0036490414:144.00233 | 100:6000   | HCD                                        | 1               | B03    |                        5   |     2 |                 1 |       nan |                              nan |           nan |    nan | Trypsin/P | Specific      | False                     | Oxidation (M);Acetyl (Protein N-term) | Carbamidomethyl (C)   | False                                     | False        |              1 |                       2 | Standard         | 13344 |  118993 |     0 |            137425 |                  100557 |                       0 |                    36868 |              48931 |                    47151 |                        0 |                      1780 |                     36 |                           47 |                            0 |                           4.8 |                          35470 | 1968826 |            111792 |                   5.7 |                         2231 |                              2   |             296137 |                        92837 |                              91437 |                               31 |                                     34 |                                    6567 |                                         7.1 | +              |                             0.74379 |                         1.0626  |                             0.48075 |                         0.72643 |
| 2018_09_28_13_00_Q-Exactive-HF-X-Orbitrap_6011 | MNT_2018_Proteomics/2018_09_28_13_00_Q-Exactive-HF-X-Orbitrap_6011.raw     | 3192042749 |   2.97282 |        66 | 2018-09-28 13:00:47     | Q Exactive HF-X Orbitrap             | Q Exactive HF-X Orbitrap | Exactive Series slot #6011 | 2.9-290033/2.9.0.2923 | rev. 1             |                   11372 |                  119429 |               2 |              58 |  0.00367022 |     144.001 |     300.129 |     1532.72 |        0.00367022 |               0.5 |         nan |            130801 | 1:130801        | 0.0036702249:144.0008  | 100:6000   | HCD                                        | 1               | A01    |                        2.5 |     1 |                 1 |       nan |                              nan |           nan |    nan | Trypsin/P | Specific      | False                     | Oxidation (M);Acetyl (Protein N-term) | Carbamidomethyl (C)   | False                                     | False        |              1 |                       2 | Standard         | 11372 |  119429 |     0 |            136853 |                  102005 |                       0 |                    34848 |              50287 |                    48043 |                        0 |                      2244 |                     37 |                           47 |                            0 |                           6.4 |                          37767 | 1408019 |            113534 |                   8.1 |                         3886 |                              3.4 |             201256 |                        91094 |                              89599 |                               45 |                                     49 |                                    9025 |                                         9.9 | +              |                             0.70728 |                         1.0271  |                             0.44402 |                         0.67985 |
| 2019_05_28_17_51_Q-Exactive-HF-X-Orbitrap_6096 | MNT_2019_Proteomics/MNT/2019_05_28_17_51_Q-Exactive-HF-X-Orbitrap_6096.raw | 1958832977 |   1.82431 |        66 | 2019-05-28 17:51:55     | Q Exactive HF-X Orbitrap             | Q Exactive HF-X Orbitrap | Exactive Series slot #6096 | 2.9-290033/2.9.0.2926 | rev. 1             |                   11353 |                   97342 |               2 |              60 |  0.00371359 |     144.003 |     300.145 |     1625.79 |        0.00371359 |               0.5 |         nan |            108695 | 1:108695        | 0.0037135892:144.00287 | 100:6000   | HCD                                        | 1               | C7     |                        2.5 |     2 |                 1 |       nan |                              nan |           nan |    nan | Trypsin/P | Specific      | False                     | Oxidation (M);Acetyl (Protein N-term) | Carbamidomethyl (C)   | False                                     | False        |              1 |                       2 | Standard         | 11353 |   97342 |     0 |            106758 |                   87926 |                       0 |                    18832 |              49905 |                    48385 |                        0 |                      1520 |                     47 |                           55 |                            0 |                           8.1 |                          37908 | 1399019 |             93506 |                   6.7 |                         2974 |                              3.2 |             204304 |                        79464 |                              78172 |                               39 |                                     43 |                                    7184 |                                         9   | +              |                             0.68956 |                         0.96467 |                             0.42647 |                         0.62328 |


There are three curated intensity dumps available - for the protein groups level (aggregated
using the gene sets) from [`proteinGroups.txt`](https://cox-labs.github.io/coxdocs/output_tables.html#protein-groups), the peptide level (aggregate the peptide sequence) from [`peptides.txt`](https://cox-labs.github.io/coxdocs/output_tables.html#peptide-table) and the precursors (aggregate ions - sequence + charge) from
[`evidence.txt`](https://cox-labs.github.io/coxdocs/output_tables.html#evidence-table). See a description of the MaxQuant output tables [here](https://cox-labs.github.io/coxdocs/output_tables.html).

Linked dumps in table format (FTP-Download):
- [geneGroups_aggregated.zip](https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233/geneGroups_aggregated.zip) [0.2GB] - 7,444 samples, 4,547 selected protein groups
- [peptides_aggregated.zip](https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233/peptides_aggregated.zip) [1.2 GB] - 7,444 samples, 42,723 selected peptides
- [precursors_aggregated.zip](https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233/precursors_aggregated.zip) [1.3 GB] - 7,444 samples, 49,339 selected precursors

> The aggregated dumps are best unzipped and a small script is provided in the zipped folder for loading the data.

These were build using cleaned MaxQuant output tables, which are provided here:

- [proteinGroups_single_dumps.zip](https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233/proteinGroups_single_dumps.zip) [2.5 GB] - 7,484 files (some duplicates)
- [peptides_single_dumps.zip](https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233/peptides_single_dumps.zip) [9.4 GB] - 7,444 files
- [precursors_single_dumps.zip](https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233/precursors_single_dumps.zip) [7.1 GB] - 7,444 files

These contain the filtered, but not downsampled data for each samples. You might need the 
metadata file to filter the data for your analysis.

```python
from pathlib import Path
import pandas as pd
import zipfile

# ARCHIVE = 'peptides_single_dumps.zip'
# ARCHIVE = 'precursors_single_dumps.zip'
ARCHIVE = 'proteinGroups_single_dumps.zip'

ftp_folder = 'https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233'
file = 'pride_metadata.csv'

meta = pd.read_csv(f'{ftp_folder}/{file}', index_col=0)

def len_csv_files_in_archive(archiv_path: str) -> dict:
    """Read csv files in zip and keep their length, i.e. number of features."""
    stats = dict()
    with zipfile.ZipFile(archiv_path, 'r') as zip_archive:
        for fname in zip_archive.namelist():
            # Check if the file is a csv
            if fname.endswith('.csv'):
                # Open each file
                with zip_archive.open(fname) as f:
                    df = pd.read_csv(f)
                    fname = Path(fname).stem
                    stats[fname] = len(df)
    return stats


stats = len_csv_files_in_archive(ARCHIVE)
stats = pd.Series(stats) # contains some duplicates which were removed from aggregated data.
stats = stats.loc[meta.index]
stats
```

|       |          |
|:------|---------:|
| count | 7444     |
| mean  | 3833.45  |
| std   |  698.794 |
| min   | 1196     |
| 25%   | 3390.75  |
| 50%   | 3849     |
| 75%   | 4181.25  |
| max   | 5925     |

So for the 7,444 selected samples there is a median of 3849 protein groups quantified per sample.

### Download using python

Download a file programaically using python:

```python
import urllib.request
ARCHIVE = 'proteinGroups_single_dumps.zip'

ftp_folder = 'https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233'
file = 'pride_metadata.csv'

urllib.request.urlretrieve(f'{ftp_folder}/{file}', f'{file}')
urllib.request.urlretrieve(f'{ftp_folder}/{ARCHIVE}', f'{ARCHIVE}')
```

### download on the command line
You can also downlaod the zip-archives on the command line using `curl` (which is available for Windows, MacOS, and Linux distributions):

```bash
curl -O https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233/geneGroups_aggregated.zip
curl -O https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233/peptides_aggregated.zip
curl -O https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233/precursors_aggregated.zip
curl -O https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233/proteinGroups_single_dumps.zip
curl -O https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233/peptides_single_dumps.zip
curl -O https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233/precursors_single_dumps.zip
```

Could be executed from a `.bat` or `.sh` script.

### SDRF file

```
import pandas as pd
pd.options.display.max_columns = 80

ftp_folder = 'https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233'
file = 'Experimental-Design.sdrf.tsv'

df = pd.read_table(f'{ftp_folder}/{file}', index_col=0)
df.sample(5, random_state=42).sort_index()
```

## Project

The project folder contains notebooks for data processing of MaxQaunt text output folders
and the analysis of the data for the publication, see its [README](project/README.md) for details.

## Workflows

The workflows folder in the repository contains snakemake workflows used for rawfile data processing, 
both for running MaxQuant over a large set of HeLa raw files 
and ThermoRawFileParser on a list of raw files to extract their meta data.

> [!NOTE] The metadata workflow now runs already with the PRIDE data.

### MaxQuant

Process single raw files using MaxQuant. See [README](workflows/maxquant/README.md) for details.

### Metadata

Read metadata from single raw files using MaxQuant. See [README](workflows/metadata/README.md) for details.


## Setup

Create a new environment in case you want to have a separate installation for running 

```
conda create -n hela_data -c conda-forge -c defaults python numpy matplotlib pandas plotly seaborn fastcore omegaconf ipywidgets tqdm pyyaml umap-learn scikit-learn openpyxl xmltodict papermill
# jupyterlab # maybe add a jupyterlab installation (depends on your setup)
conda activate hela_data
```

and then install the custom code (and dependencies, which should be installed already installed if you use the above environment):

```
pip install . # . for current directory which should be this repository
```

