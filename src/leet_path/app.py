import socket
import typing

import pandas as pd
from dash import Dash, dash_table

from src.data.filer import file_utils
from src.data.graphql import leet_ql
from src.leet_path.helper import scorer, path_generator, report_generator, consts


# TODO:
#   checks: lint, test coverage
#   features: persist last state, record progress (bulk import, single entries, edit errors)


def _get_all_problems() -> pd.DataFrame:
    df = leet_ql.get_all_questions()
    df[consts.SCORE] = scorer.evaluate(df)
    return df


def _get_solved_problems(file_name: str) -> typing.Iterable:
    return [int(x) for x in file_utils.read_txt(file_name).split('\n')]


def _dew_it(input_file, problems_file, report_file, todo_file):
    res = _get_all_problems()
    file_utils.write_sheet(problems_file, res)

    solved = _get_solved_problems(input_file)
    res = report_generator.append_solved(res, solved)
    report_generator.print_progress_summary(res)
    file_utils.write_sheet(report_file, res)

    res = path_generator.get_low_hanging_fruit(res)
    file_utils.write_sheet(todo_file, res)
    return res


if __name__ == '__main__':
    app = Dash()
    todo_df = _dew_it('0. Solved.txt', '1. LeetCode.xlsx', '2. LeetReport.xlsx', '3. LeetPath.xlsx').reset_index()
    app.layout = dash_table.DataTable(todo_df.to_dict('records'), [{"name": i, "id": i} for i in todo_df.columns])
    app.run(host=socket.gethostbyname(socket.gethostname()), port=9000)
