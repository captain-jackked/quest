import os
from pathlib import Path

import pandas as pd

from src.common import collection_utils, project_config

DEFAULT_FILER = 'dump/'


def use_path(fn):
    def _get_project_dir():
        file_path_components = str(Path(__file__)).split('\\')
        project_name_position = collection_utils.find_last_occurrence(file_path_components, project_config.PROJECT_NAME)
        return '/'.join(file_path_components[:1 + project_name_position])

    def _generate_path(file_name: str):
        location = Path(os.path.join(_get_project_dir(), DEFAULT_FILER))
        location.mkdir(parents=True, exist_ok=True)
        return os.path.join(location, file_name)

    def decorated(*args, **kwargs):
        file_name, *args = args
        return fn(_generate_path(file_name), *args, **kwargs)

    return decorated


@use_path
def write_sheet(file_name: str, /, data: dict | pd.DataFrame):
    if isinstance(data, pd.DataFrame):
        data = {str(file_name).split('\\')[-1]: data}
    with pd.ExcelWriter(file_name) as writer:
        for sheet_name, table in data.items():
            table.to_excel(writer, sheet_name=sheet_name)


@use_path
def read_sheet(file_name: str, /) -> dict | pd.DataFrame:
    return pd.read_excel(file_name, index_col=0)


@use_path
def read_txt(file_name: str, /) -> str:
    with open(file_name) as file:
        res = file.read()
    return res


@use_path
def delete_file(file_name: str, /):
    os.remove(file_name)
