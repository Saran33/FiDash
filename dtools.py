
import os
import pandas as pd
import pandas_datareader.data as web
# from alpha_vantage.timeseries import TimeSeries
# from pwe.av import get_av_ts
# from datetime import datetime, timedelta
# import pytz
# import pwe.pwetools as pwe
from pwe.pwetools import check_folder, dt_to_str, sort_index

# end_date = pytz.utc.localize(datetime.utcnow())
# str_end = pwe.dt_to_str(end_date)
# print("END:", end_date)
# start_date = (end_date - timedelta(days=365))
# str_start = pwe.dt_to_str(start_date)
# print("START", start_date)

# Find securities functions

# os.environ["IEX_API_KEY"] =
# os.environ["ALPHAVANTAGE_API_KEY"] =

def wdr_ticker(ticker, start_date, end_date, source='stooq', save_csv=False):
    """
    Use web datareader to return a df of secutity price data.

    https://pandas-datareader.readthedocs.io/en/latest/remote_data.html
    """

    print('')
    # print("Security:", ticker)
    print('')

    tkr = ticker.replace('/', '_')

    print("Checking if a file for this ticker with the same start and end dates exists...")
    # csv_start, csv_end = get_file_datetime(start_date, end_date)
    csv_start = dt_to_str(start_date)
    csv_end = dt_to_str(end_date)

    check_folder('csv_files')

    relpath = f'csv_files/{tkr}_{csv_start}_{csv_end}.csv'
    file_path = os.path.abspath(relpath)
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
        if len(df)>2:
            df = sort_index(df, utc=True)
            df.index.names = ['DateTime']
            print (f"DOWNLOADED: {ticker}")
            print (df[:5])

            if save_csv:
                print (relpath)
                df.to_csv(relpath, index=True)
                abs_path = os.path.abspath(relpath)
                print ("Saved data to:",abs_path)
        else:
            print (f"No data found for {ticker}")

    return df


def wdr_multi_ticker(tickers, start_date, end_date, source='stooq', price='Close', save_csv=False):
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
    # csv_start, csv_end = get_file_datetime(start_date, end_date)
    csv_start = dt_to_str(start_date)
    csv_end = dt_to_str(end_date)

    df_list = []
    missing_secs = []
    check_folder('csv_files')

    for tkr in tkrs:
        relpath = f'csv_files/{tkr}_{csv_start}_{csv_end}.csv'
        file_path = os.path.abspath(relpath)
        if os.path.exists(file_path) == True:

            print("Matching local file exists.")
            print("Reading recent file from CSV...")
            print(file_path)

            df = pd.read_csv(file_path, low_memory=False, index_col=[
                            'DateTime'], parse_dates=['DateTime'], infer_datetime_format=True)
            # df = sort_index(df, utc=False)
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
            if len(df)>2:
                df = sort_index(df, utc=True)
                df.index.names = ['DateTime']
                print (f"DOWNLOADED: {tkr}")
                print (df[:5])

                if save_csv:
                    print (relpath)
                    df.to_csv(relpath, index=True)
                    abs_path = os.path.abspath(relpath)
                    print ("Saved data to:",abs_path)

                df = df[[price]]
                df = df.rename(columns={price: tkr})
                df_list.append(df)
            else:
                print (f"No data found for {tkr}")
                missing_secs.append(tkr)
            
        # dfs = dfs.join(df)
        if df_list:
            dfs = pd.concat(df_list, axis=1)
        else:
            dfs = pd.DataFrame()

    return dfs, missing_secs

def indexed_vals(df):
    return df.pct_change().fillna(0).add(1).cumprod().mul(100)


def ext_str_lst(str_list):
    return ", ".join(map(str, str_list))