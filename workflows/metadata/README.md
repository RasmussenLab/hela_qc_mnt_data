# Metadata workflow

Get metadata from ThermoFischer proteomics raw files using
[`ThermoRawFileParser`](https://github.com/compomics/ThermoRawFileParser)

> :warning: On unix systems, make sure that mono is available

## Output

- both json and txt data format into `jsons` and `txts` folder
- create combined `rawfile_metadata.json` (needs to be deleted if files are added)

## Configfile

add a `config/files.yaml` in [config](config):

```yaml
out_folder: metadata
out_csv: metadata_rawfiles.csv
thermo_raw_file_parser_exe: mono /projects/rasmussen/people/kzl465/hela_qc_mnt_data/ThermoRawFileParser1.4.4/ThermoRawFileParser.exe
files:
  - 2013_04_03_16_54_Q-Exactive-Orbitrap_1
  - 2013_04_03_17_47_Q-Exactive-Orbitrap_1
ftp_folder: pride/data/archive/2023/12/PXD042233
ftp_prefix: ftp://
ftp_server: ftp.pride.ebi.ac.uk
folder_raw: tmp_rawfiles
excluded:
- 
```

### Add files on PRIDE to config file

> Already done for PRIDE, but could be used to select a subset of the files.

The list of files is extracted from [`pride_metadata.csv`](https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233/pride_metadata.csv).

```python
from pathlib import PurePosixPath as Path
import yaml
import pandas as pd
pd.options.display.max_columns = 80

ftp_folder = 'https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233'
file = 'pride_metadata.csv'

config_file = 'config/files.yaml'

df = pd.read_csv(f'{ftp_folder}/{file}', index_col=0)

with open(config_file) as f:
    config = yaml.safe_load(f)

config['files'] = df.index.to_list()

with open(config_file, 'w') as f:
    yaml.dump(config, f)
```

Then invoke the workflow with the list of config files

```bash
# dry-run
snakemake --configfiles config/files.yaml config/excluded.yaml -p -n
```

### Excluded files

Some files might be corrupted and not be processed by `ThermoRawFileParser`. These can be
excluded based on the `tmp` folder

```bash 
# check files
echo 'excluded:' > config/excluded_$(date +"%Y%m%d").yaml
find  tmp -name '*.raw*' | awk 'sub(/^.{4}/," ? ")' >> config/excluded_$(date +"%Y%m%d").yaml

# potentially add these to the workflow exclusion files:
find  tmp -name '*.raw*' | awk 'sub(/^.{4}/," ? ")' >> config/excluded.yaml
# rm -r tmp/* # remove excluded files
# add to files.yaml
```

these files are ignored in the workflow (configured as a python set) after adding these
to the `config/files.yaml`.

## Setup

- download and unzip [`ThermoRawFileParser`](https://github.com/compomics/ThermoRawFileParser)
- add path to `exe` to config

```bash
# sudo apt-get update
sudo apt install mono-complete
conda create -n snakemake snakemake
conda activate snakemake
snakemake -n  # see job listing
```

## zip outputs


```bash
# could be part of snakemake process
zip -r metadata.zip txt jsons
```