from snakemake.script import snakemake
import json
import pandas as pd

use_sdrf_columsn = ['source name',  # sample_accession
                    'characteristics[organism]',  # condition
                    'characteristics[biological replicate]',  # biological_replicate
                    'comment[technical replicate]'  # run
                    ]
rename_columns = {'source name': 'sample_accession',
                  'characteristics[organism]': 'condition',
                  'characteristics[biological replicate]': 'biological_replicate',
                  'comment[technical replicate]': 'run'
                  }

ftp_folder = 'https://ftp.pride.ebi.ac.uk/pride/data/archive/2023/12/PXD042233'
file = 'Experimental-Design.sdrf.tsv'

sdrf = pd.read_table(f'{ftp_folder}/{file}', usecols=use_sdrf_columsn)
sdrf = sdrf.rename(columns=rename_columns).convert_dtypes()
sdrf.sample(5, random_state=42).sort_index().T


parquets = snakemake.input.parquet_files
with open('parquet_files/parquet_files.json', 'w') as f:
    json.dump(parquets, f)

# subselect for testing
# parquets = snakemake.input.parquet_files[:10]

data = list()
for file in parquets:
    df = pd.read_parquet(file)
    data.append(df.convert_dtypes())
del df
data = pd.concat(data, ignore_index=True)

data = data.join(sdrf.set_index('sample_accession'), on='sample_accession', how='left')

data.to_parquet('parquet_files/PXD042233_peptides.parquet', index=False)

