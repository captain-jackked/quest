import numpy as np
import pandas as pd

from src.common import leet_consts

MODIFIED_ACC = 'Modified Acceptance'
BASE_SCORES = {leet_consts.EASY: 1.0, leet_consts.MEDIUM: 2.0, leet_consts.HARD: 3.0}


def _get_adjustment(acc: pd.Series) -> pd.Series:
    def _get_slope(x, y) -> float:
        m, _ = np.polyfit(x, y, 1)
        return m

    indices, values, pivot = acc.keys().values, acc.values, len(acc) // 2
    left_slope, right_slope = _get_slope(indices[:pivot], values[:pivot]), _get_slope(indices[pivot:], values[pivot:])
    # adj_values = [(pivot - i) * (left_slope if i < pivot else right_slope) for i in indices]  # pull up
    adj_values = [-(min(i, pivot) - 1) * left_slope + (max(0, i - pivot)) * (-right_slope) for i in
                  indices]  # push down
    return pd.Series(data=adj_values, index=indices)


def _append_modified_acc(df: pd.DataFrame):
    df[MODIFIED_ACC] = df[leet_consts.ACCEPTANCE] + _get_adjustment(df[leet_consts.ACCEPTANCE])
    df[MODIFIED_ACC] = np.maximum(np.minimum(df[MODIFIED_ACC], 0.99), 0.01)
    ans = []
    for diff in BASE_SCORES.keys():
        df_diff = df[df[leet_consts.DIFFICULTY] == diff]
        avg_acc = df_diff[MODIFIED_ACC].mean()
        ans.append((avg_acc - df_diff[MODIFIED_ACC]) / (1 - avg_acc))  # (rejection - avg_rej) / avg_rej
    df[MODIFIED_ACC] = pd.concat(ans).squeeze()


def _get_score_multiplier(modified_acc: float) -> float:
    return 1 + modified_acc


def _get_score(df: pd.DataFrame) -> pd.Series:
    ans = []
    for diff, base_score in BASE_SCORES.items():
        df_diff = df[df[leet_consts.DIFFICULTY] == diff]
        ans.append(df_diff[MODIFIED_ACC].apply(lambda x: base_score * _get_score_multiplier(x)))
    return pd.concat(ans).squeeze()


def evaluate(df: pd.DataFrame) -> pd.Series:
    df = df.copy(deep=True)
    _append_modified_acc(df)
    return _get_score(df)
