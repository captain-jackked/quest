import os
import typing

import pandas as pd


def write_sheet(data: typing.Union[pd.DataFrame, dict[pd.DataFrame]], file_name: str):
    if isinstance(data, pd.DataFrame):
        data = {file_name: data}
    with pd.ExcelWriter(file_name) as writer:
        for sheet_name, table in data.items():
            table.to_excel(writer, sheet_name=sheet_name)


def read_sheet(file_name: str) -> typing.Union[pd.DataFrame, dict[pd.DataFrame]]:
    return pd.read_excel(file_name, index_col=0)


def delete_file(file_name: str):
    os.remove(file_name)
