from typing import Dict

import numpy as np
import pandas as pd


class CandlesFeatures:


    @staticmethod
    def candles_last_combined_features_of(candles_by_periods: Dict[str, pd.DataFrame],
                                     cnt_by_period: Dict[str, int]) -> pd.DataFrame:
        # todo: optimize
        return CandlesFeatures.candles_combined_features_of(candles_by_periods, cnt_by_period).tail(1)

    @staticmethod
    def candles_combined_features_of(candles_by_periods: Dict[str, pd.DataFrame],
                                     cnt_by_period: Dict[str, int]) -> pd.DataFrame:
        """ Combine feature columns from fast and slow candles to single dataframe """
        if not candles_by_periods:
            return pd.DataFrame()

        merged = None
        for period, candles in candles_by_periods.items():
            features = CandlesFeatures.candles_features_of(candles_by_periods[period], period, cnt_by_period[period])
            merged = pd.merge_asof(merged, features, left_index=True, right_index=True) \
                if merged is not None else features
        return merged.dropna()

    @staticmethod
    def candles_features_of(candles: pd.DataFrame, interval: str, window_size: int):
        cols = ["open", "high", "low", "close", "vol"]
        features = candles.copy().reset_index(drop=True)[cols + ["close_time"]]

        # Add previous window candles to columns
        for i in range(1, window_size):
            prefix = f"{interval}_-{i}_"
            for col in cols:
                features[prefix + col] = features.shift(i)[col]
        features.set_index("close_time", inplace=True, drop=True)

        # Add prefix to ohlcv columns
        for col in cols:
            features.rename(columns={col: f"{interval}_{col}"}, inplace=True)

        return features.diff().dropna()
