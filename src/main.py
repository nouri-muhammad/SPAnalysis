from data.sp_list import SP500, CompanyFilter
from data.storage import save_to_csv
from data.yfinance_api import YFinanceManager


sp500 = SP500()

table = sp500.fetch_companies()

energy_filter = CompanyFilter(
    table, 
    sector="Energy"
)
energy_companies = energy_filter.save_companies()

no_filter = CompanyFilter(
    table=table
)
all_companies = no_filter.save_companies()

yfm = YFinanceManager(
    company_list_file="data/raw/Energy/Energy.csv",
    interval="1h",
    sector="energy_companies"
)

yfm.download_all()
