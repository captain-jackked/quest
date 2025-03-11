import typing

import pandas as pd

from src.common import leet_consts
from src.data.filer import file_utils
from src.data.graphql import leet_ql
from src.quant import leet_utils


# TODO:
#   checks: lint, test coverage
#   features: persist last state, record progress (bulk import, single entries, edit errors)

def _get_all_problems() -> pd.DataFrame:
    return leet_utils.append_leetcode_metrics(leet_ql.get_all_questions())


def _get_solved_problems(file_name: str) -> typing.Iterable:
    return [int(x) for x in file_utils.read_txt(file_name).split('\n')]


def _append_solved(problems: pd.DataFrame, solved: typing.Iterable) -> pd.DataFrame:
    problems = problems.copy(deep=True)
    problems[leet_consts.SOLVED] = ''
    for index in solved:
        problems.at[index, leet_consts.SOLVED] = 1
    return problems


if __name__ == '__main__':
    df = _append_solved(_get_all_problems(), _get_solved_problems('Solved.txt'))
    file_utils.write_sheet('Leet-Sheet.xlsx', df)
