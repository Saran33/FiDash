
import os
import pandas as pd
import pandas_datareader.data as web
from alpha_vantage.timeseries import TimeSeries
from pwe.av import get_av_ts
from datetime import datetime, timedelta
import pytz
import pwe.pwetools as pwe

end_date = pytz.utc.localize(datetime.utcnow())
str_end = pwe.dt_to_str(end_date)
print("END:", end_date)
start_date = (end_date - timedelta(days=30))
str_start = pwe.dt_to_str(start_date)
print("START", start_date)

# Find securities functions

# os.environ["IEX_API_KEY"] =
# os.environ["ALPHAVANTAGE_API_KEY"] =

def wdr_ticker(ticker, start_date, end_date, source='stooq'):
    """
    Use web datareader to return a df of secutity price data.

    https://pandas-datareader.readthedocs.io/en/latest/remote_data.html
    """

    print('')
    # print("Security:", ticker)
    print('')

    tkr = ticker.replace('/', '_')

    print("Checking if a file for this ticker with the same start and end dates exists...")
    # csv_start, csv_end = pwe.get_file_datetime(start_date, end_date)
    csv_start = str_start
    csv_end = str_end

    file_path = os.path.abspath(
        f'csv_files/{tkr}_{csv_start}_{csv_end}.csv')
    if os.path.exists(file_path) == True:

        print("Matching local file exists.")
        print("Reading recent file from CSV...")
        print(file_path)

        df = pd.read_csv(file_path, low_memory=False, index_col=[
                         'DateTime'], parse_dates=['DateTime'], infer_datetime_format=True)
        df.name = f"{tkr}"

    else:
        print(f"No CSV: {file_path} found. Downloading data from {source} API")

        df = pd.DataFrame(web.DataReader(ticker, source, start=start_date,
                            end=end_date))  # ['AMZN', 'GOOGL',] api_key=os.getenv('ALPHAVANTAGE_API_KEY')
        # df=df.melt(ignore_index=False, value_name="price").reset_index()
        # df = df.stack().reset_index()
        df = pwe.sort_index(df, utc=True)
        df.index.names = ['DateTime']
        df[:15]

        df.to_csv(file_path, index=True)

    return df


def wdr_multi_ticker(tickers, start_date, end_date, source='stooq', price='Close'):
    """
    Use web datareader to return a df of secutity price data.

    https://pandas-datareader.readthedocs.io/en/latest/remote_data.html
    """

    print('')
    # print("Securities:", tickers)
    print('')

    tkrs = []
    for t in tickers:
        tkr = t.replace('/', '_')
        tkrs.append(tkr)

    print("Checking if ticker files exist locally...")
    # csv_start, csv_end = pwe.get_file_datetime(start_date, end_date)
    csv_start = str_start
    csv_end = str_end

    df_list = []

    for tkr in tkrs:
        file_path = os.path.abspath(
            f'csv_files/{tkr}_{csv_start}_{csv_end}.csv')
        if os.path.exists(file_path) == True:

            print("Matching local file exists.")
            print("Reading recent file from CSV...")
            print(file_path)

            df = pd.read_csv(file_path, low_memory=False, index_col=[
                            'DateTime'], parse_dates=['DateTime'], infer_datetime_format=True)
            # df = pwe.sort_index(df, utc=False)
            df = df[[price]]
            df = df.rename(columns={price: tkr})
            # df.name = f"{tkr}"
            df_list.append(df)

        else:
            print(f"No CSV for {tkr} found. Downloading data from {source} API")
            df = pd.DataFrame(web.DataReader(tkr, source, start=start_date,
                                end=end_date))
            # df=df.melt(ignore_index=False, value_name="price").reset_index()
            # df = df.stack().reset_index()
            df = pwe.sort_index(df, utc=True)
            df.index.names = ['DateTime']
            df[:15]

            df.to_csv(file_path, index=True)

            df = df[[price]]
            df = df.rename(columns={price: tkr})
            df_list.append(df)
            
        # dfs = dfs.join(df)
        if df_list:
            dfs = pd.concat(df_list, axis=1)

    return dfs

def indexed_vals(df):
    return df.pct_change().fillna(0).add(1).cumprod().mul(100)


