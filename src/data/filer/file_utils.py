import os
import sys
import typing
from pathlib import Path

import pandas as pd

DEFAULT_FILER = 'dump/'


def use_path(fn):
    def _get_project_dir():
        syspath = sys.path
        for x in syspath[1:]:
            if x in syspath[0]:
                return x
        return syspath[0]

    def _generate_path(file_name: str):
        location = Path(os.path.join(_get_project_dir(), DEFAULT_FILER))
        location.mkdir(parents=True, exist_ok=True)
        return os.path.join(location, file_name)

    def decorated(*args, **kwargs):
        file_name, *args = args
        return fn(_generate_path(file_name), *args, **kwargs)

    return decorated


@use_path
def write_sheet(file_name: str, /, data: typing.Union[pd.DataFrame, dict]):
    if isinstance(data, pd.DataFrame):
        data = {str(file_name).split('\\')[-1]: data}
    with pd.ExcelWriter(file_name) as writer:
        for sheet_name, table in data.items():
            table.to_excel(writer, sheet_name=sheet_name)


@use_path
def read_sheet(file_name: str, /) -> typing.Union[pd.DataFrame, dict]:
    return pd.read_excel(file_name, index_col=0)


@use_path
def read_txt(file_name: str, /) -> str:
    with open(file_name) as file:
        res = file.read()
    return res


@use_path
def delete_file(file_name: str, /):
    os.remove(file_name)
