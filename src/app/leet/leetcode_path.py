import pandas as pd

from data import leet_graphql
from quant import metric_utils


# TODO:
#   checks: lint, test coverage
#   features: persist last state, record progress (bulk import, single entries, edit errors)

def get_questions() -> pd.DataFrame:
    return metric_utils.append_leetcode_metrics(leet_graphql.get_all_questions_raw())


if __name__ == '__main__':
    print(get_questions())
