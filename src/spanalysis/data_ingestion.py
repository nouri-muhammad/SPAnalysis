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
    def __init__(self):
        self.data_path = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("initiating the data ingestion method.")

        try:

            for file_path in self.data_path.data_path.glob("*.csv"):
                df = pd.read_csv(filepath_or_buffer=file_path)
                df["Datetime"] = pd.to_datetime(df["Datetime"], utc=True)
                logging.info(f"Read the {file_path} csv file")

                tscv = TimeSeriesSplit(n_splits=100, test_size=1)
                for fold, (train_index, test_index) in  enumerate(tscv.split(df), start=1):
                    train = df[['Close']].iloc[train_index]
                    test = df[['Close']].iloc[test_index]

                    # print(train_index, test_index)
                    logging.info(
                        f"Fold {fold}: "
                        f"Train={len(train)} observations "
                        # f"({df['Datetime'].iloc[train_index[0]]} → "
                        # f"{df['Datetime'].iloc[train_index[-1]]}), "
                        f"Test={len(test)} observations "
                        # f"({df['Datetime'].iloc[test_index[0]]} → "
                        # f"{df['Datetime'].iloc[test_index[-1]]})"
                    )
            return train, test

                    #TODO: Here the data should be sent to data transformation and then to the model selection class to find the best fitting model
            
        except Exception as e:
            raise CustomException(e, sys)


if __name__=="__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
