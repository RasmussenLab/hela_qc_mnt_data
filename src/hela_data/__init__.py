# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

# put into some pandas_cfg.py file and import all
import pandas as pd
import pandas.io.formats.format as pf

import hela_data.plotting
from hela_data.plotting import savefig
import hela_data.pandas

logging.getLogger(__name__).addHandler(NullHandler())

__license__ = 'GPLv3'
__version__ = (0, 1, 0)


class IntArrayFormatter(pf.GenericArrayFormatter):
    def _format_strings(self):
        formatter = self.formatter or '{:,d}'.format
        fmt_values = [formatter(x) for x in self.values]
        return fmt_values


pd.options.display.float_format = '{:,.3f}'.format
pf.IntArrayFormatter = IntArrayFormatter


