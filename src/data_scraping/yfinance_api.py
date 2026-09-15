import pandas as pd
import yfinance as yf
import datetime as dt

from pathlib import Path
from data_scraping.storage import read_from_csv, save_to_csv


class YFinanceManager:
    LIMITS = {
        "1m": dt.timedelta(days=6),
        "5m": dt.timedelta(days=59),
        "15m": dt.timedelta(days=59),
        "30m": dt.timedelta(days=59),
        "1h": dt.timedelta(days=719),
        "1d": dt.timedelta(days=1799)
    }

    def __init__(self, company_list_file, look_back_days: int | None = None, interval: str = '1h', \
                 output_dir: str | Path = "data/company_data", sector: str | None=None):
        self.company_list_file = company_list_file
        self.interval = self.interval_validation(interval)
        self.look_back_days = look_back_days
        self.start = self.get_start_date(self.look_back_days, self.interval)
        self.end = self.get_latest_date()
        self.table = read_from_csv(self.company_list_file)
        if self.table is None:
            raise ValueError("There is no table to get tickers from")
        self.output_dir =  Path(output_dir)
        self.sector = sector

    @classmethod
    def interval_validation(cls, interval):
        """
        Checks if the interval inserted by the user is allowed by yfinance standards.
        Args:
            interval (_type_): the inserted interval by user. 

        Returns:
            _type_: If there is no problem with the interval, it returns the interval to be saved.
        """
        if interval in cls.LIMITS.keys():
            return interval
        else:
            raise ValueError("interval must be one of {1m, 2m, 5m, 15m, 30m, 1h, 1d}")
            #TODO: otherwise it returns the default of 15m.
            # try:
            #     input(f"The {interval} is not allowed. Should the 1 hour interval be used as the default? ")
            # except:
            #     pass

    @staticmethod
    def get_latest_date():
        """
        Determines the current date and converts it to a string. 
        Returns:
            _type_: A string.
        """
        return dt.date.today().strftime("%Y-%m-%d")

    @classmethod
    def get_start_date(cls, look_back_days, interval):
        """
        Determines the start date for collecting data.
        Args:
            look_back_days (_type_): how many days back should it look for
            interval (_type_): the interval between data points

        Returns:
            _type_: The start time or an error if the inserted date is not supported by yfinance.
        """
        if look_back_days is None:
            start = dt.date.today() - cls.LIMITS[interval]
            return start
        elif look_back_days <= cls.LIMITS[interval].days:
            start = dt.date.today() - dt.timedelta(days=look_back_days)
            return start
        else:
            raise ValueError(
                f"look back days cannot exceed {cls.LIMITS[interval].days}\
                    for interval {interval}"
            )

    def get_tickers(self) -> list[str]:
        """
        Gets and returns the list of tickers.
        Returns:
            list[str]: list of tickers.
        """
        return self.extract_tickers(self.table)

    def extract_tickers(self, table: pd.DataFrame) -> list[str]:
        """
        Extracts the list of tickers from the scraped table.
        Args:
            table (pd.DataFrame): the list of all companies present in SP500

        Returns:
            list[str]: list of tickers
        """
        return table["Symbol"].tolist()

    def download_ticker(self, ticker: str) -> pd.DataFrame|None:
        """
        Gets the data regarding the ticker passed on to it from yfinance if it is not delisted. 
        Args:
            ticker (str): the company's Symbol

        Returns:
            pd.DataFrame|None: the financial history.
        """
        ticker_obj = yf.Ticker(ticker)
        print(f"Downloading {ticker}...")
        history = ticker_obj.history(
            start=self.start,
            end=self.end,
            interval=self.interval
        )
        if history.empty:
            print(f"No ticker_obj is available for {ticker}")
            #TODO check if the list of companies has changed and update it. Ticker no longer exists.
            return None
        return history

    def build_output_path(self, ticker: str) -> Path:
        """
        Builds an output path to save the result.
        Args:
            ticker (str): the symbol of the company

        Returns:
            Path: file path to save the result.
        """
        base_dir = Path(self.output_dir)
        print(base_dir)
        if self.sector:
            filepath = base_dir/f"{self.sector}"/f"{ticker}.csv"
        else:
            filepath = base_dir/"SP500"/f"{ticker}.csv"
        filepath.parent.mkdir(parents=True, exist_ok=True) 
        print(filepath)
        return filepath

    def download_all(self) -> None:
        """
        Iterates over the list of tickers and pass them to download_ticker to get the financial data
        and saves each one. 
        """
        tickers = self.get_tickers()
        for ticker in tickers:
            try:
                data = self.download_ticker(ticker)
                if data is None:
                    continue
                filepath = self.build_output_path(ticker)
                save_to_csv(data, filepath, index=True)
            except Exception as e:
                print(f"Failed to download {ticker}: {e}")
                #TODO check if the list of companies has changed and update it. Ticker no longer exists. 
            