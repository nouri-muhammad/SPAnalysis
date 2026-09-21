from data_scraping.sp_list import SP500, CompanyFilter
from data_scraping.storage import save_to_csv
from data_scraping.yfinance_api import YFinanceManager

from spanalysis.data_ingestion import DataIngestion
from spanalysis.data_transformation import DataTransformation



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


ingestion_obj = DataIngestion()
train_data, test_data = ingestion_obj.initiate_data_ingestion()

transform_obj = DataTransformation(train=train_data, test=test_data)
train_array, test_array, preprocessing_obj = transform_obj.initiate_data_transformation()
print(train_array)