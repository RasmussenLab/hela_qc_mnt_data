# Run ibaqpy using the quantmsio_format (parquet)


In order to try [ibaqpy](https://github.com/bigbio/ibaqpy) on this large hela dataset,
we creata one parquet file as specified in quantms.io 
([peptide quantification feature](https://github.com/bigbio/quantms.io/blob/dev/docs/feature.rst)).

## Procedure

I will first have create the parquet file as specified in quantms.io using
a Snakemake workflow.

```bash
snakemake -c1 --use-conda
```

the script [scripts/maxquant_convert.py](scripts/maxquant_convert.py) is specific to this dataset and
- encodes the peptide sequence as ProForma with the two modifications in the dataset
- write the data to a parquet file
- write the dat to a csv file (optional)


Then the parsed files are aggregated into a joint `parquet` file along the 
sample data information from the SDRF file using: [scripts/merge_files.py](scripts/merge_files.py)

