import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, select, asc, desc, func
import logging
import time
from TickerScrape.models import Security, AssetClass, Country, Currency, Industry, Exchange, Tag

# uri = 'sqlite:///databases/TickerScrape.db'
uri = 'sqlite:////Users/zenman618/Documents/git_packages/VisualStudioGit/TickerScrape/sqlite_files/TickerScrape.db'

def init_engine(uri):
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    engine = create_engine(uri)
    return engine

def db_connect(engine):
    connection = engine.connect()
    logging.info("****_Ticker_Pipeline: database connected****")
    return connection

def db_session(engine):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    session = Session(engine)
    logging.info("****_Ticker_Pipeline: database connected****")
    return session

engine = init_engine(uri)

def all_tickers():
    with db_session(engine) as session:
        result = session.execute("select ticker, name from security")
        df = pd.DataFrame(result, columns = ['Ticker', 'Name'])
        df['Label'] = df['Ticker'] + " (" + df['Name'] + ")"
        symbols = df['Ticker']
        labels = df['Label']
    return labels, symbols


