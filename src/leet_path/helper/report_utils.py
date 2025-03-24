import typing

import pandas as pd

from src.leet_path.helper import consts


def append_solved(problems: pd.DataFrame, solved: typing.Iterable) -> pd.DataFrame:
    problems = problems.copy(deep=True)
    problems[consts.SOLVED] = False
    for index in solved:
        problems.at[index, consts.SOLVED] = True
    problems = problems[consts.OUTPUT_COLS]
    return problems


def print_progress_summary(df: pd.DataFrame):
    def _get_count(raw: pd.DataFrame, flt):
        return len(raw[flt])

    def _get_scores(raw: pd.DataFrame, flt):
        return sum(raw[flt][consts.SCORE])

    solved_flt, premium_flt = df[consts.SOLVED], df[consts.PREMIUM]
    for difficulty in [consts.EASY, consts.MEDIUM, consts.HARD]:
        diff_flt = df[consts.DIFFICULTY] == difficulty
        print('{:>7}: {:>7}/{:<4} (Solved/Total) | Unsolved: {:>4}/{:<4} (Non-premium/Premium)'.format(
            difficulty,
            _get_count(df, diff_flt & solved_flt), _get_count(df, diff_flt),
            _get_count(df, diff_flt & ~solved_flt & ~premium_flt), _get_count(df, diff_flt & ~solved_flt & premium_flt)
        ))
    print('{:>7}: {:>7.1f}/{:.0f} (Solved/Total)'.format(
        'Score', _get_scores(df, solved_flt), _get_scores(df, [True] * len(df.index))
    ))
    print('-' * 80)
