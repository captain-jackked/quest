import numpy as np
import pandas as pd

from src.common import leet_consts

MODIFIED_ACC = 'Modified Acceptance'
BASE_SCORES = {leet_consts.EASY: 1.0, leet_consts.MEDIUM: 2.0, leet_consts.HARD: 3.0}

RAMP_END = 1200
SLOPE = 44 / 3e5


def _linear_offset(seed_values: pd.Series, limit: int, slope: float):
    # TODO: remove hard-coding of the adjustment OR remove adjustment
    return np.minimum(seed_values, limit) * slope


def _append_modified_acc(df: pd.DataFrame):
    df[MODIFIED_ACC] = df[leet_consts.ACCEPTANCE] - _linear_offset(df.index, RAMP_END, SLOPE)
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
