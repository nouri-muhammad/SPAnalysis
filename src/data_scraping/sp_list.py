import os
import pandas as pd
import requests

from io import StringIO
from pathlib import Path

from data_scraping.storage import save_to_csv

SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


class SP500:
    def __init__(self):
        pass

    def fetch_companies(self) -> pd.DataFrame:
        """
        This method gets the data in sp500 table from wikipedia page. 
        
        Returns:
            pd.DataFrame: the infromation of all companies in sp500 in pandas dataframe format.
        """
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            SP500_URL,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()
        table = pd.read_html(StringIO(response.text))[0]
        return table


class CompanyFilter():
    def __init__(self, table: pd.DataFrame, sector: str | None=None, output_dir: str | Path = "data/raw"):
        """
        Filters the companies read from Wikipedia by sector and save the new list.
        Args:
            table (_type_): dataset in pandas dataframe format which is gotten from SP500.fetch_companies() method. 
            sector (str | None, optional): The desired sector if it is mentioned by the user. Defaults to None.
            output_dir (str | Path, optional): The directory file is saved in. Defaults to "data/raw".
        """
        self.table = table
        self.sector = sector
        self.output_dir = output_dir

    def build_output_path(self, ticker: str) -> Path:
        """
        This function creates a Path object to save the files.
        Args:
            ticker (str): name of the file

        Returns:
            Path: a Path object 
        """
        if self.sector:
            base_dir = Path(self.output_dir)
            filepath = base_dir/f"{self.sector}"/f"{ticker}.csv"
        else:
            base_dir = Path(self.output_dir)
            filepath = base_dir/"SP500"/f"{ticker}.csv"

        filepath.parent.mkdir(parents=True, exist_ok=True) 
        return filepath

    def filter_by_sector(self) -> pd.DataFrame:
        """
        Filters the table by sector.
        Raises:
            ValueError: _description_

        Returns:
            pd.DataFrame: _description_
        """
        filtered = self.table[self.table["GICS Sector"] == self.sector]
        if filtered.empty:
            raise ValueError("You probably have misspelled the sector name.")
        return filtered 

    def save_companies(self) -> None:
        """
        This method first calls the filter method, and filters the list by sector, if a sector is specified.
        It uses no filter if no sector is inputed. 
        Then it calls the save method to save the result in a csv file in data.raw directory
        """
        if self.sector is None:
            data = self.table
            filename = "sp500"
        else:
            data = self.filter_by_sector()
            filename = self.sector

        filepath = self.build_output_path(filename)
        save_to_csv(data, filepath)
