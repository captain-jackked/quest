import typing

import pandas as pd

from src.data.filer import file_utils


def generate_random_df():  # TODO: add params (id_lim=10, col_lim=10)
    return pd.DataFrame([[1, 2], [3, 4]], index=['a', 'b'], columns=['c', 'd'])


def setup_test_files(gen_config: typing.Union[None, dict[str, typing.Callable]]) -> typing.Callable:
    def decorated(func: typing.Callable) -> typing.Callable:
        def simply_decorated(*args, **kwargs):
            for gen_name, gen_func in gen_config.items():
                file_utils.write_sheet(gen_name, gen_func())
            res = func(*args, **kwargs)
            for gen_name in gen_config.keys():
                file_utils.delete_file(gen_name)
            return res

        return simply_decorated

    return decorated
