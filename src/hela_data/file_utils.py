from pathlib import Path
import logging

import pandas as pd

import xmltodict
from numpy import dtype

logger = logging.getLogger('src.file_utils.py')


MQ_VERSION = '1.6.12.0'


def check_for_key(iterable, key):
    """Check for key in items of Iterable
    using `in`(`__contains__`).

    Parameters
    ----------
    iterable : Iterable of Strings
        Iterable of items which the key can be checked for
    key : String
        key to check for using `key in item` of Iterable.

    Returns
    -------
    string, int
        Returns zero if nothing is found, otherwise a string.
        If only one item is found containing the key, return this.
        Multiple hits are returned connacotaed using an underscore.
    """
    hits = [x for x in iterable if key in x]
    n_hits = len(hits)
    if n_hits == 1:
        return hits[0]
    elif n_hits == 0:
        return 0
    elif n_hits > 1:
        return '_'.join(iterable)


# can file-loading be made concurrent?
# check tf.data


def load_summary(filepath: str = 'summary.txt') -> pd.DataFrame:
    """Load MaxQuant {MQ_VERSION} summary.txt file.

    Parameters
    ----------
    filepath : str, optional
        filepath, by default 'summary.txt'

    Returns
    -------
    pd.DataFrame
        Text-File is returned as pandas.DataFrame
    """.format(MQ_VERSION=MQ_VERSION)
    df = pd.read_table(filepath)
    df = df.T
    df = df.iloc[:, :-1]
    return df


def load_mqpar_xml(filepath: Path) -> dict:
    """Load MaxQuant {MQ_VERSION}parameter file in xml format which stores parameters for MaxQuant run,
    including version numbers.

    Parameters
    ----------
    filepath : str, optional
        filepath to xml- parameter file

    Returns
    -------
    dict
        XML-File parsed as dictionary
    """.format(MQ_VERSION=MQ_VERSION)
    with open(filepath) as f:
        _ = f.readline()
        xml = f.read()

    return xmltodict.parse(xml)


types_peptides = {'N-term cleavage window': dtype('O'),
                  'C-term cleavage window': dtype('O'),
                  'Amino acid before': dtype('O'),
                  'First amino acid': dtype('O'),
                  'Second amino acid': dtype('O'),
                  'Second last amino acid': dtype('O'),
                  'Last amino acid': dtype('O'),
                  'Amino acid after': dtype('O'),
                  'A Count': dtype('int64'),
                  'R Count': dtype('int64'),
                  'N Count': dtype('int64'),
                  'D Count': dtype('int64'),
                  'C Count': dtype('int64'),
                  'Q Count': dtype('int64'),
                  'E Count': dtype('int64'),
                  'G Count': dtype('int64'),
                  'H Count': dtype('int64'),
                  'I Count': dtype('int64'),
                  'L Count': dtype('int64'),
                  'K Count': dtype('int64'),
                  'M Count': dtype('int64'),
                  'F Count': dtype('int64'),
                  'P Count': dtype('int64'),
                  'S Count': dtype('int64'),
                  'T Count': dtype('int64'),
                  'W Count': dtype('int64'),
                  'Y Count': dtype('int64'),
                  'V Count': dtype('int64'),
                  'U Count': dtype('int64'),
                  'O Count': dtype('int64'),
                  'Length': dtype('int64'),
                  'Missed cleavages': dtype('int64'),
                  'Mass': dtype('float64'),
                  'Proteins': dtype('O'),
                  'Leading razor protein': dtype('O'),
                  'Start position': dtype('float64'),
                  'End position': dtype('float64'),
                  'Gene names': dtype('O'),
                  'Protein names': dtype('O'),
                  'Unique (Groups)': dtype('O'),
                  'Unique (Proteins)': dtype('O'),
                  'Charges': dtype('O'),
                  'PEP': dtype('float64'),
                  'Score': dtype('float64'),
                  'Intensity': dtype('int64'),
                  'Reverse': dtype('O'),
                  'Potential contaminant': dtype('O'),
                  'id': dtype('int64'),
                  'Protein group IDs': dtype('O'),
                  'Mod. peptide IDs': dtype('O'),
                  'Evidence IDs': dtype('O'),
                  'MS/MS IDs': dtype('O'),
                  'Best MS/MS': dtype('float64'),
                  'Oxidation (M) site IDs': dtype('O'),
                  'MS/MS Count': dtype('int64')}


dtypes_proteins = {'Protein IDs': dtype('O'),
                   'Majority protein IDs': dtype('O'),
                   'Peptide counts (all)': dtype('O'),
                   'Peptide counts (razor+unique)': dtype('O'),
                   'Peptide counts (unique)': dtype('O'),
                   'Protein names': dtype('O'),
                   'Gene names': dtype('O'),
                   'Fasta headers': dtype('O'),
                   'Number of proteins': dtype('int64'),
                   'Peptides': dtype('int64'),
                   'Razor + unique peptides': dtype('int64'),
                   'Unique peptides': dtype('int64'),
                   'Sequence coverage [%]': dtype('float64'),
                   'Unique + razor sequence coverage [%]': dtype('float64'),
                   'Unique sequence coverage [%]': dtype('float64'),
                   'Mol. weight [kDa]': dtype('float64'),
                   'Sequence length': dtype('int64'),
                   'Sequence lengths': dtype('O'),
                   'Q-value': dtype('float64'),
                   'Score': dtype('float64'),
                   'Intensity': dtype('int64'),
                   'MS/MS count': dtype('int64'),
                   'Only identified by site': dtype('O'),
                   'Reverse': dtype('O'),
                   'Potential contaminant': dtype('O'),
                   'id': dtype('int64'),
                   'Peptide IDs': dtype('O'),
                   'Peptide is razor': dtype('O'),
                   'Mod. peptide IDs': dtype('O'),
                   'Evidence IDs': dtype('O'),
                   'MS/MS IDs': dtype('O'),
                   'Best MS/MS': dtype('O'),
                   'Oxidation (M) site IDs': dtype('O'),
                   'Oxidation (M) site positions': dtype('O'),
                   'Taxonomy IDs': dtype('O')}


def load_protein_intensities(filepath):
    """Load Intensities from `proteins.txt`.
    Data types of columns as of in MaxQuant {MQ_VERSION}

    Parameters
    ----------
    filepath : str
        filepath (rel or absolute) to MQ proteins.txt

    Returns
    -------
    pandas.DataFrame
        Return text file as DataFrame.
    """.format(MQ_VERSION=MQ_VERSION)
    df = pd.read_table(
        filepath, index_col='Majority protein IDs', dtype=dtypes_proteins)
    return df[['Intensity']]
