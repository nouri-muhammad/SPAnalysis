import os
import sys

import numpy as np
import pandas as pd

from dataclasses import dataclass
from pathlib import Path
from sklearn.model_selection import TimeSeriesSplit

from exception import CustomException
from logger import logging


@dataclass
class DataIngestionConfig:
    data_path = Path('data/company_data/energy')


class DataIngestion:
    def __init__(self, df):
        self.df = df

    def initiate_data_ingestion(self):
        logging.info("initiating the data ingestion method.")

        try:
            tscv = TimeSeriesSplit(n_splits=100, test_size=1)
            for fold, (train_index, test_index) in  enumerate(tscv.split(self.df), start=1):
                train = self.df.iloc[train_index]
                test = self.df.iloc[test_index]

                # logging.info(
                #     f"Fold {fold}: "
                #     f"Train={len(train)} observations,"
                #     # f"({df['Datetime'].iloc[train_index[0]]} → "
                #     # f"{df['Datetime'].iloc[train_index[-1]]}), "
                #     f"Test={len(test)} observations,"
                #     # f"({df['Datetime'].iloc[test_index[0]]} → "
                #     # f"{df['Datetime'].iloc[test_index[-1]]})"
                # )
                # logging.info(f"Yielding Fold: {fold}, train={len(train)}, and test={len(test)} observation")
                yield (
                    train,
                    test
                )

        except Exception as e:
            raise CustomException(e, sys)


if __name__=="__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
