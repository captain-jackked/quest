import socket
import typing

import pandas as pd
from dash import Dash, html

from src.data.filer import file_utils
from src.data.graphql import leet_ql
from src.leet_path.helper import score_utils, path_utils, report_utils, consts, ui_utils


# TODO: Generic
#   pipeline, test coverage, pylint
#   deploy - heroku (or alternates), also [docker & kubernetes]?

# TODO: Features
#   persist last state - all problems and current profile solved
#   record progress - bulk import, single entries, edit entries


def _get_all_problems() -> pd.DataFrame:
    df = leet_ql.get_all_questions()
    df[consts.SCORE] = score_utils.evaluate(df)
    return df


def _get_solved_problems() -> typing.Iterable:
    return [int(x) for x in file_utils.read_txt('0. Solved.txt').split('\n')]


def _generate_layout():
    all_problems = _get_all_problems()
    file_utils.write_sheet('1. LeetCode.xlsx', all_problems)

    solved = _get_solved_problems()
    solved_report = report_utils.append_solved(all_problems, solved)
    report_utils.print_progress_summary(solved_report)
    file_utils.write_sheet('2. LeetReport.xlsx', solved_report)

    leet_path = path_utils.get_low_hanging_fruit(solved_report)
    file_utils.write_sheet('3. LeetPath.xlsx', leet_path)

    return html.Div([
        ui_utils.generate_table(all_problems),
        ui_utils.generate_table(leet_path),
    ])


if __name__ == '__main__':
    app = Dash()
    app.layout = _generate_layout()
    app.run(host=socket.gethostbyname(socket.gethostname()), port=9000)
