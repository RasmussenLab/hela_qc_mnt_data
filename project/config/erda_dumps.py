from pathlib import Path
ROOT_DUMPS = Path("path/to/data")

FN_PROTEIN_GROUPS = ROOT_DUMPS / 'geneGroups' / 'intensities_wide_selected_N07444_M04547.pkl'
FN_PEPTIDES = ROOT_DUMPS / 'peptides' / 'intensities_wide_selected_N07444_M42723.pkl'
FN_EVIDENCE = ROOT_DUMPS / 'precursors' / 'intensities_wide_selected_N07444_M49339.pkl'

ERDA_DUMPS = [FN_EVIDENCE, FN_PEPTIDES, FN_PROTEIN_GROUPS]
