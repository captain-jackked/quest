import typing

import pandas as pd

from src.common import leet_consts

BASE_SCORES = {leet_consts.EASY: 1.0, leet_consts.MEDIUM: 2.0, leet_consts.HARD: 4.0}
AVG_WINDOW = 500
DECAY_RATE = 2
DECAY_FLOOR = 0.5


def _get_rolling_acceptance(df: pd.DataFrame, window) -> pd.Series:
    return df.rolling(window=window, min_periods=0, center=True)[leet_consts.ACCEPTANCE].mean()


def _get_de_skewed_acceptance(df: pd.DataFrame) -> pd.Series:
    return df[leet_consts.ACCEPTANCE] - df[leet_consts.ACC_ROLL_AVG]


def _get_normalized_acceptance(df: pd.DataFrame, difficulties: typing.Iterable) -> pd.Series:
    ans = []
    for diff in difficulties:
        df_diff = df[df[leet_consts.DIFFICULTY] == diff]
        avg_acc, std_acc = df_diff[leet_consts.ACC_DE_SKEWED].mean(), df_diff[leet_consts.ACC_DE_SKEWED].std()
        ans.append(df_diff[leet_consts.ACC_DE_SKEWED].apply(lambda x: (x - avg_acc) / std_acc))
    return pd.concat(ans).squeeze()


def _get_score(df: pd.DataFrame, base_scores: dict, decay_rate: float, decay_floor: float) -> pd.Series:
    def _acc_to_score(normalized_acc: float, b_score: float, decay_r: float, decay_f: float) -> float:
        decay_factor = decay_f + (1 - decay_f) * decay_r ** (-abs(normalized_acc))
        if normalized_acc < 0:  # is_tougher
            decay_factor = 1 / decay_factor
        return b_score * decay_factor

    ans = []
    for diff, score in base_scores.items():
        df_diff = df[df[leet_consts.DIFFICULTY] == diff]
        ans.append(
            df_diff[leet_consts.ACC_NORMALIZED].apply(lambda x: _acc_to_score(x, score, decay_rate, decay_floor)))
    return pd.concat(ans).squeeze()


def append_leetcode_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy(deep=True)
    df[leet_consts.ACC_ROLL_AVG] = _get_rolling_acceptance(df, AVG_WINDOW)
    df[leet_consts.ACC_DE_SKEWED] = _get_de_skewed_acceptance(df)
    df[leet_consts.ACC_NORMALIZED] = _get_normalized_acceptance(df, BASE_SCORES.keys())
    df[leet_consts.SCORE] = _get_score(df, BASE_SCORES, DECAY_RATE, DECAY_FLOOR)
    return df
