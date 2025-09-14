import socket
import typing

from dash import Dash, html

from src.data.filer import file_utils
from src.playground.leet_path import score_utils, sheet_utils, consts, ui_utils, leet_graph_ql
from src.playground.leet_path.table_filter import FilterFactory


# TODO: Generic
#   pipeline, test coverage, pylint
#   deploy - heroku (or alternates), also [docker & kubernetes]?

# TODO: Features
#   persist last state - all problems and current profile solved
#   record progress - bulk import, single entries, edit entries


def _get_solved_problems() -> typing.Iterable:
    return set(int(x) for x in file_utils.read_txt('0. Solved.txt').split('\n'))


def _generate_layout():
    all_problems = leet_graph_ql.get_all_questions()

    solved = _get_solved_problems()
    solved_report = all_problems.assign(**{consts.SOLVED: all_problems.index.isin(solved)})
    solved_report[consts.SCORE] = score_utils.evaluate(solved_report)
    sheet_utils.print_progress_summary(solved_report)

    filters = {
        consts.SOLVED: False,
        consts.PREMIUM: False,
        consts.TAGS: {'values': ['NA', 'shell'], 'flip': True},
    }
    leet_path = solved_report
    for flt in FilterFactory.get_filters(filters):
        leet_path = flt.apply(leet_path)
    leet_path = leet_path.sort_values(by=[consts.SCORE])

    export_config = {
        '1. LeetCode.xlsx': all_problems,
        '2. LeetReport.xlsx': solved_report,
        '3. LeetPath.xlsx': leet_path
    }
    for k, v in export_config.items():
        file_utils.write_sheet(k, sheet_utils.beautify(v, style=sheet_utils.EXCEL))

    components = []
    for v in [all_problems, leet_path]:
        components.append(ui_utils.generate_table(
            sheet_utils.beautify(v, style=sheet_utils.MARKDOWN),
            md_cols=[consts.TITLE],
            pct_cols=[consts.ACCEPTANCE],
            dec_cols=[consts.SCORE],
        ))
    return html.Div(components)


if __name__ == '__main__':
    app = Dash()
    app.layout = _generate_layout()
    app.run(host=socket.gethostbyname(socket.gethostname()), port=9000)
