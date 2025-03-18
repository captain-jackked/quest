from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from src.common import leet_consts


class LeetScorer(ABC):
    MODIFIED_ACC = 'Modified Acceptance'
    BASE_SCORES = {leet_consts.EASY: 1.0, leet_consts.MEDIUM: 2.0, leet_consts.HARD: 3.0}

    WINDOW = 1200
    RAMP_END = WINDOW
    SLOPE = 44 / 3e5

    @classmethod
    def _window_avg(cls, values: pd.Series, window: int):
        return values.rolling(window=window, min_periods=0, center=True).mean()

    @classmethod
    def _linear_offset(cls, seed_values: pd.Series, limit: int, slope: float):
        return np.minimum(seed_values, limit) * slope

    @classmethod
    @abstractmethod
    def _append_modified_acc(cls, df: pd.DataFrame):
        pass

    @classmethod
    @abstractmethod
    def _get_score_multiplier(cls, modified_acc: float) -> float:
        pass

    @classmethod
    def _get_score(cls, df: pd.DataFrame) -> pd.Series:
        ans = []
        for diff, base_score in cls.BASE_SCORES.items():
            df_diff = df[df[leet_consts.DIFFICULTY] == diff]
            ans.append(df_diff[cls.MODIFIED_ACC].apply(lambda x: base_score * cls._get_score_multiplier(x)))
        return pd.concat(ans).squeeze()

    @classmethod
    def _run_template(cls, df: pd.DataFrame) -> pd.Series:
        df = df.copy(deep=True)
        cls._append_modified_acc(df)
        return cls._get_score(df)

    @classmethod
    def eval(cls, df: pd.DataFrame) -> pd.Series:
        return cls._run_template(df)


class WindowedScorer(LeetScorer):
    DECAY_RATE = 2
    DECAY_FLOOR = 0.5

    @classmethod
    def _append_modified_acc(cls, df: pd.DataFrame):
        df[cls.MODIFIED_ACC] = df[leet_consts.ACCEPTANCE] - cls._window_avg(df[leet_consts.ACCEPTANCE], cls.WINDOW)
        ans = []
        for diff in cls.BASE_SCORES.keys():
            df_diff = df[df[leet_consts.DIFFICULTY] == diff]
            avg_acc, std_acc = df_diff[cls.MODIFIED_ACC].mean(), df_diff[cls.MODIFIED_ACC].std()
            ans.append(df_diff[cls.MODIFIED_ACC].apply(lambda x: (x - avg_acc) / std_acc))
        df[cls.MODIFIED_ACC] = pd.concat(ans).squeeze()

    @classmethod
    def _get_score_multiplier(cls, modified_acc: float) -> float:
        decay_factor = cls.DECAY_FLOOR + (1 - cls.DECAY_FLOOR) * cls.DECAY_RATE ** (-abs(modified_acc))
        return decay_factor if modified_acc >= 0 else 1 / decay_factor


class RejectionScorer(LeetScorer):
    @classmethod
    def _append_modified_acc(cls, df: pd.DataFrame):
        df[cls.MODIFIED_ACC] = df[leet_consts.ACCEPTANCE] - cls._linear_offset(df.index, cls.RAMP_END, cls.SLOPE)
        # df[cls.MODIFIED_ACC] = df[leet_consts.ACCEPTANCE] - cls._window_avg(df[leet_consts.ACCEPTANCE], cls.WINDOW)
        ans = []
        for diff in cls.BASE_SCORES.keys():
            df_diff = df[df[leet_consts.DIFFICULTY] == diff]
            avg_acc = df_diff[cls.MODIFIED_ACC].mean()
            ans.append((avg_acc - df_diff[cls.MODIFIED_ACC]) / (1 - avg_acc))  # (rejection - avg_rej) / avg rej
        df[cls.MODIFIED_ACC] = pd.concat(ans).squeeze()

    @classmethod
    def _get_score_multiplier(cls, modified_acc: float) -> float:
        return 1 + modified_acc
