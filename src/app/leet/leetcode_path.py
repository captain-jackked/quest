import typing

import pandas as pd

from src.common import leet_consts
from src.data import leet_graphql
from src.quant import metric_utils


# TODO:
#   checks: lint, test coverage
#   features: persist last state, record progress (bulk import, single entries, edit errors)

def _get_all_problems() -> pd.DataFrame:
    return metric_utils.append_leetcode_metrics(leet_graphql.get_all_questions())


def _get_solved_problems(filename: str) -> typing.Iterable:
    with open(filename) as file:
        res = file.read()
    return [int(x) for x in res.split('\n')]


def _append_solved(problems: pd.DataFrame, solved: typing.Iterable) -> pd.DataFrame:
    problems = problems.copy(deep=True)
    problems[leet_consts.SOLVED] = False
    for index in solved:
        problems.at[index, leet_consts.SOLVED] = True
    return problems


if __name__ == '__main__':
    df = _append_solved(_get_all_problems(), _get_solved_problems('Solved.txt'))
    df.to_excel('Leet-Sheet.xlsx')
