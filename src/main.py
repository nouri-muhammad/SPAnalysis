from data_scraping.sp_list import SP500, CompanyFilter
from data_scraping.storage import save_to_csv
from data_scraping.yfinance_api import YFinanceManager

from spanalysis.data_ingestion import DataIngestion
from spanalysis.data_transformation import DataTransformation
from logger import logging


sp500 = SP500()

table = sp500.fetch_companies()

energy_filter = CompanyFilter(
    table, 
    sector="Energy"
)
energy = energy_filter.save_companies()

finance_filter = CompanyFilter(
    table, 
    sector="Financials"
)
financial = finance_filter.save_companies()

no_filter = CompanyFilter(
    table=table
)
all_companies = no_filter.save_companies()

yfm = YFinanceManager(
    company_list_file="data/raw/Energy/Energy.csv",
    interval="1h",
    sector="energy"
)

yfm.download_all()

yfm = YFinanceManager(
    company_list_file="data/raw/Financials/Financials.csv",
    interval="1h",
    sector="financial"
)

yfm.download_all()

# all the data is downloaded and processing begins

transform_obj = DataTransformation()

for file_path, clean_df in transform_obj.initiate_data_transformation():
    logging.info("Starting ingestion for {file_path}")
    ingestion_obj = DataIngestion(df=clean_df)

    for train, test in ingestion_obj.initiate_data_ingestion():
        pass
        # logging.info(
        #     f"{file_path.name}: "
        #     f"train={len(train)}, "
        #     f"test={len(test)}"
        # )
