import typing

import pandas as pd

from src.common import leet_consts
from src.data.filer import file_utils
from src.data.graphql import leet_ql
from src.quant import leet_utils


# TODO:
#   checks: lint, test coverage
#   features: persist last state, record progress (bulk import, single entries, edit errors)


def _get_solved_problems(file_name: str) -> typing.Iterable:
    return [int(x) for x in file_utils.read_txt(file_name).split('\n')]


def _append_solved(problems: pd.DataFrame, solved: typing.Iterable) -> pd.DataFrame:
    problems = problems.copy(deep=True)
    problems[leet_consts.SOLVED] = ''
    for index in solved:
        problems.at[index, leet_consts.SOLVED] = 'Yes'
    return problems


def _dew_it() -> pd.DataFrame:
    df = leet_ql.get_all_questions()
    df = leet_utils.append_leetcode_metrics(df)
    df = _append_solved(df, _get_solved_problems('Solved.txt'))
    return df


def _get_count(df: pd.DataFrame, flt):
    return len(df[flt])


def _get_scores(df: pd.DataFrame, flt):
    return sum(df[flt][leet_consts.OLD_SCORE])


def _print_summary(df: pd.DataFrame):
    solved_flt, premium_flt = df[leet_consts.SOLVED] != '', df[leet_consts.PREMIUM]
    for difficulty in [leet_consts.EASY, leet_consts.MEDIUM, leet_consts.HARD]:
        diff_flt = df[leet_consts.DIFFICULTY] == difficulty
        diff_probs, solved_diff, unsolved_diff_prem, unsolved_diff_non_prem = [_get_count(df, flt) for flt in (
            diff_flt,
            diff_flt & solved_flt,
            diff_flt & ~solved_flt & ~premium_flt,
            diff_flt & ~solved_flt & premium_flt
        )]
        print('{}: {}/{} (Solved/Total), Pending: {}/{} (Non-premium/Premium)'.format(
            difficulty,
            solved_diff, diff_probs,
            unsolved_diff_non_prem, unsolved_diff_prem
        ))
    all_probs, solved = (_get_scores(df, flt) for flt in ([True] * len(df.index), solved_flt))
    print(f'Score: {solved:.1f}/{all_probs:.1f} (Solved/Total)')


if __name__ == '__main__':
    res = _dew_it()
    _print_summary(res)
    file_utils.write_sheet('Leet-Sheet.xlsx', res)
