import typing

import pandas as pd

from src.common import leet_consts
from src.common.table_filter import TableFilter
from src.data.filer import file_utils
from src.data.graphql import leet_ql
from src.quant import leet_scorer


# TODO:
#   checks: lint, test coverage
#   features: persist last state, record progress (bulk import, single entries, edit errors)


def _get_all_problems() -> pd.DataFrame:
    df = leet_ql.get_all_questions()
    df[leet_consts.SCORE] = leet_scorer.evaluate(df)
    return df


def _get_solved_problems(file_name: str) -> typing.Iterable:
    return [int(x) for x in file_utils.read_txt(file_name).split('\n')]


def _append_solved(problems: pd.DataFrame, solved: typing.Iterable) -> pd.DataFrame:
    problems = problems.copy(deep=True)
    problems[leet_consts.SOLVED] = False
    for index in solved:
        problems.at[index, leet_consts.SOLVED] = True
    problems = problems[leet_consts.OUTPUT_COLS]
    return problems


def _print_progress_summary(df: pd.DataFrame):
    def _get_count(raw: pd.DataFrame, flt):
        return len(raw[flt])

    def _get_scores(raw: pd.DataFrame, flt):
        return sum(raw[flt][leet_consts.SCORE])

    solved_flt, premium_flt = df[leet_consts.SOLVED], df[leet_consts.PREMIUM]
    for difficulty in [leet_consts.EASY, leet_consts.MEDIUM, leet_consts.HARD]:
        diff_flt = df[leet_consts.DIFFICULTY] == difficulty
        print('{:>7}: {:>7}/{:<4} (Solved/Total) | Unsolved: {:>4}/{:<4} (Non-premium/Premium)'.format(
            difficulty,
            _get_count(df, diff_flt & solved_flt), _get_count(df, diff_flt),
            _get_count(df, diff_flt & ~solved_flt & ~premium_flt), _get_count(df, diff_flt & ~solved_flt & premium_flt)
        ))
    print('{:>7}: {:>7.1f}/{:.0f} (Solved/Total)'.format(
        'Score', _get_scores(df, solved_flt), _get_scores(df, [True] * len(df.index))
    ))
    print('-' * 80)


def _get_low_hanging_fruit(report: pd.DataFrame):
    _print_progress_summary(report)

    report = TableFilter(leet_consts.SOLVED, False).apply(report)
    report = TableFilter(leet_consts.PREMIUM, False).apply(report)
    report = TableFilter(leet_consts.TAGS, ['NA', 'shell'], flip=True).apply(report)
    return report.sort_values(by=[leet_consts.SCORE])


def _dew_it(input_file, problems_file, report_file, todo_file):
    res = _get_all_problems()
    file_utils.write_sheet(problems_file, res)

    res = _append_solved(res, _get_solved_problems(input_file))
    file_utils.write_sheet(report_file, res)

    res = _get_low_hanging_fruit(res)
    file_utils.write_sheet(todo_file, res)


if __name__ == '__main__':
    _dew_it('0. Solved.txt', '1. LeetCode.xlsx', '2. LeetReport.xlsx', '3. LeetPath.xlsx')
