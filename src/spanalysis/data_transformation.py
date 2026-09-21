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

class DataTransformation:
    def __init__(self, train, test):
        """
        This class creates transformer objects and transofrms train data.
        Args:
            train (_type_): train data
        """
        self.train = train
        self.test = test
        self.feature = ["Close"]

    def interpolate_neighbors(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        This method fills the null values based on the average of the previous and next value in the dataset.
        Args:
            X (_type_): dataframe - train or test data

        Returns:
            _type_: data frame with no null values, sent to mdoel selection.
        """
        return X.interpolate(
            method='linear', 
            limit_direction='both'
        )

    def data_transformer_object(self):
        """
        This method is responsible for performing data transformation - Standard-Scaling. 
        """
        try:

            data_pipleline = Pipeline(
                steps=[
                    ("imputer", FunctionTransformer(self.interpolate_neighbors)),
                ]
            )
            logging.info("data transformation pipeline is created.")

            preprocessor = ColumnTransformer(
                [
                    ("data_pipleline", data_pipleline, self.feature)
                ]
            )
            logging.info("column transformer is initiated.")

            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self):
        try:
            preprocessing_obj = self.data_transformer_object()
            logging.info("preprocessing object is created.")

            train_array = preprocessing_obj.fit_transform(self.train)
            logging.info("Training data successfully transformed.")

            test_array = preprocessing_obj.transform(self.test)
            logging.info("Test data successfully transformed.")

            return (
                train_array, 
                test_array, 
                preprocessing_obj
            )

        except Exception as e:
            raise CustomException(e, sys)
