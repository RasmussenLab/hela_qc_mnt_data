"""Convert Maxquant evidence table to quantmsio format.

Script is specific to the data. would need to extent modification encoding for
other datasets.
"""
import argparse
# %%
from collections import defaultdict
from pathlib import Path

import pandas as pd


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Convert Maxquant evidence table to quantmsio format')
    parser.add_argument('--input_file', '-i', type=str, help='Path to the input evidence.txt file')
    parser.add_argument('--output_file', '-o', type=str, help='Path to the output parquet file')
    return parser.parse_args()


# peptide field schema for peptide records
#
fields_peptide = {
    "name": "peptide",
    "type": "record",
    "fields": [
            {"name": "sequence", "type": "string"},
            {"name": "protein_accessions", "type": {
                "type": "array", "items": "string"}},
            {"name": "unique", "type": "int"},
            # '"Andromeda:Score": 120.1'
            {"name": "best_id_score", "type": "double"},
            {"name": "reference_file_name", "type": "string"},
            {"name": "modifications", "type": {"type": "array", "items": "string"}},
            {"name": "retention_time", "type": "float"},
            {"name": "charge", "type": "int"},
            {"name": "exp_mass_to_charge", "type": "double"},
            {"name": "scan_number", "type": "string"},
            {"name": "sample_accession", "type": "string"},
            {"name": "abundance", "type": "float"},
            {"name": "peptidoform", "type": "string"},
            {"name": "number_of_psms", "type": "int"},
            {"name": "is_decoy", "type": "int"},
            {"name": "posterior_error_probability", "type": "double"},
            {"name": "consensus_support", "type": "float"},
            {"name": "id_scores", "type": {"type": "array", "items": "string"}},
            {"name": "gene_accessions", "type": {
                "type": "array", "items": "string"}},
            {"name": "gene_names", "type": {"type": "array", "items": "string"}
             }
    ]
}

# mapping evidence table columns to the fields in the schema
# https://cox-labs.github.io/coxdocs/output_tables.html#evidence-table
map_column_names = {
    'Sequence': 'sequence',
    'Proteins': 'protein_accessions',
    # unique: if proteins has length one
    'Score': 'best_id_score',  # '{"Andromeda":Score}'
    'PEP': 'posterior_error_probability',
    'Modifications': 'modifications',
    'Charge': 'charge',
    'm/z': 'exp_mass_to_charge',
    'Modified sequence': 'peptidoform',
    'Raw file': 'sample_accession',  # needs to be rename for HeLa dataset
    'Intensity': 'abundance',
    'Reverse': 'is_decoy',

    # Optional fiels:
    'MS/MS IDs': 'number_of_psms',  # number_of_psms
    'Calibrated retention time': 'retention_time',
    # ? gene_accessions
    'Gene names': 'gene_names',
    # ? consensus_support
    # ? id_scores
    # ? reference_file_name
    # ? scan_number
}

use_columns = list(map_column_names.keys())

mod_rename = {
    '(Acetyl (Protein N-term))': '[Acetyl]-',
    '(Oxidation (M))': '[Oxidation]',
}

map_to_unimod = {
    'Acetyl': '1',
    'Oxidation': '35',
}


def find_pos_of_oxidation(s: str) -> str:
    """Encode oxidation in peptide sequence."""
    pos = 0
    ret = defaultdict(list)
    record_mod = False
    # s = s.replace('[Acetyl]-', '')  # remove N-term acetylation
    for c in s:
        if c == '[':
            record_mod = True
            mod = ''
        elif c == ']':
            record_mod = False
            ret[mod] += [str(pos)]
        elif record_mod:
            mod += c
        elif c == '-':
            continue
        else:
            pos += 1
    ret = ['|'.join(v) + '-UNIMOD:{}'.format(map_to_unimod[k])
           for k, v in ret.items()]
    return ret


def read_and_parse_evidence(filepath: str) -> pd.DataFrame:
    """Read and parse Maxquant evidence table to quantms.io format.

    Parameters
    ----------
    filepath : str
        evidence.txt file path

    Returns
    -------
    pd.DataFrame
        pandas DataFrame with parsed data
    """
    filepath = Path(filepath)
    df = pd.read_table(filepath, low_memory=False,
                       usecols=use_columns + ['Potential contaminant'])
    df = df.query('`Potential contaminant`!="+"')
    df = df.drop('Potential contaminant', axis=1)
    df = df.rename(columns=map_column_names)
    df['protein_accessions'] = df['protein_accessions'].str.split(';')
    df['unique'] = df['protein_accessions'].dropna().apply(len) == 1
    df['is_decoy'] = df['is_decoy'].replace({'+': True}).fillna(False)
    df['number_of_psms'] = df['number_of_psms'].str.split(';').apply(len)
    df['best_id_score'] = df['best_id_score'].apply(
        lambda x: f'"Andromeda:Score": {x}')
    for k, v in mod_rename.items():
        print(k, v)
        df['peptidoform'] = df['peptidoform'].str.replace(k, v)
    df['peptidoform'] = df['peptidoform'].str[1:-1]
    df['modifications'] = df['peptidoform'].apply(find_pos_of_oxidation)
    # rename sample_accession to filename (was changed for HeLa dataset)
    df['sample_accession'] = f"{filepath.parent}.raw"
    # optimize dtypes
    # df = df.convert_dtypes()
    df = df.astype({'charge': 'Int8', 'number_of_psms': 'Int8'})
    return df


def main(fname, fname_out) -> None:
    df = read_and_parse_evidence(fname)
    df.to_parquet(fname_out, index=False)
    df.to_pickle(fname_out.replace('.parquet', '.pkl'))


if __name__ == '__main__':
    args = parse_arguments()
    print(args)
    main(args.input_file, args.output_file)

# # %%

# # %%
# t = 'DNSTM[Oxidation]GYM[Oxidation]MAK'  # 5|8-UNIMOD:35'
# t = '[Acetyl]-M[Oxidation]M[Oxidation]CGAPSATQPATAETQHIADQVR'  # ['0-UNIMOD:1', '1|2-UNIMOD:35']

# find_pos_of_oxidation(t)


# # %%
# fname = 'DDA-LFQ-MQ/2020_06_29_14_29_Orbitrap-Exploris-480_MA10132C/evidence.txt'
# df = read_and_parse_evidence(fname)
# examples = df.astype({'modifications': 'string'}).groupby('modifications').sample(1).iloc[:, :3]
# # df['modifications'] = df['peptidoform'].apply(find_pos_of_oxidation)
# examples

# # %%
# df.loc[examples.index, :'peptidoform'].T.to_dict()

# # %%
# fact = 1024**3


# def get_memory_usage_in_gb(df: pd.DataFrame) -> float:
#     """Return memory usage in GB."""
#     return df.memory_usage(deep=True).sum() / fact


# # %%
# df = df.convert_dtypes()
# df
# # %%
# get_memory_usage_in_gb(df) * 7_444
# # %%
