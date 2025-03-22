import typing

import pandas as pd


class TableFilter:
    @staticmethod
    def _parse_valid_values(values):
        if not isinstance(values, typing.Iterable) or isinstance(values, (str, dict)):
            values = [values]
        return set(x for x in values if x is not None), None in values

    def __init__(self, col, values, flip=False):
        self.col = col
        self.values, self.has_na = TableFilter._parse_valid_values(values)
        self.flip = flip

    def _get_flt(self, df: pd.DataFrame):
        flt = df[self.col].isin(self.values)
        if self.has_na:
            flt = flt | df[self.col].isna()
        if self.flip:
            flt = ~flt
        return flt

    def apply(self, df: pd.DataFrame):
        return df[self._get_flt(df)]
