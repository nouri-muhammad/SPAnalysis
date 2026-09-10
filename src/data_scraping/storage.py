import pandas as pd

from pandas.errors import ParserError
from pathlib import Path


def save_to_csv(
        data: pd.DataFrame,
        filename: str,
        index: bool = False
) -> None:
    """
    This function saves the extracted data about the companies in a csv format.

    Args:
        data (pd.DataFrame): data regarding the companies.
        filename (str): the name, the file is intended to be saved into. 
    """
    filepath = Path(filename)

    filepath.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    data.to_csv(
        filepath,
        index=index
    )


def read_from_csv(
        filename: str
) -> pd.DataFrame | None:
    """
    This function reads the data from csv file. 

    Args:
        filename (str): The location of the file

    Returns:
        pd.DataFrame: The data in a pandas dataframe.
    """
    try:
        filepath = Path(filename)
        data = pd.read_csv(filepath)
        return data
    except (FileNotFoundError, ParserError, PermissionError) as e:
        print("could not find the file...")
        print(f"The error: {e}")
        return None
