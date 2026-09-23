import os
import sys

import numpy as np
import pandas as pd

from dataclasses import dataclass
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer 
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

from exception import CustomException
from logger import logging

"""
Strategy: 1. Relative Differencing (Recommended for Linear/Tree Models)

When to Use: If using XGBoost, LightGBM, ARIMA, or Linear Regression.

How it Works: Transform your entire raw dataset using Percentage Change (df.pct_change()) or Log Differencing. This instantly converts all trending data into stationary returns. You can then safely apply a single global StandardScaler to everything.


Strategy: 2. Local Window Scaling (Recommended for Deep Learning)

When to Use: If using LSTMs, Transformers, DeepAR, or Temporal Convolutional Networks.

How it Works: Inside your model's data generator/dataset class, grab the X lookback window. Compute its local mean and standard deviation. Divide the window by these stats, and use those same stats to scale the target Y value.
"""


@dataclass
class DataTransformationConfig:
    data_path = Path('data/company_data/energy')


class DataTransformation:
    def __init__(self) -> pd.DataFrame:
        """
        This class creates transformer objects and clean the entire data. 
        The data does not need any specific transformation, thus, we just check for null values. 
        Args:
            feature (str): target column name
        """
        self.data_path = DataTransformationConfig()

    def interpolate_neighbors(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        This method fills the null values based on the average of the previous and next value in the dataset.
        Args:
            X (pd.DataFrame): data set

        Returns:
            pd.DataFrame: data frame with no null values, ready for fold train-test split
        """
        return X.interpolate(
            method='linear', 
            limit_direction='both'
        )


    def initiate_data_transformation(self):
        try:

            for file_path in self.data_path.data_path.glob("*.csv"):
                df = pd.read_csv(filepath_or_buffer=file_path)
                df["Datetime"] = pd.to_datetime(df["Datetime"], utc=True)
                logging.info(f"Read the {file_path} csv file")

                df['Close'] = self.interpolate_neighbors(df['Close'])
                logging.info("{file_path} successfully transformed.")

                logging.info(f"Yielding the datafram {file_path}")
                yield (
                    file_path,
                    df
                )

        except Exception as e:
            raise CustomException(e, sys)
