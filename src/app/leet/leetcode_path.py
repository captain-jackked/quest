import pandas as pd

from data import leet_graphql
from quant import metric_utils


# TODO:
#   checks: lint, test coverage
#   features: persist last state, record progress (bulk import, single entries, edit errors)

def get_all_questions() -> pd.DataFrame:
    return metric_utils.append_leetcode_metrics(leet_graphql.get_all_questions())


if __name__ == '__main__':
    get_all_questions().to_excel('Leet-Sheet.xlsx')
