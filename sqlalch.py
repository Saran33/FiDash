import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, select, asc, desc, func
import logging
import time
import os
# from TickerScrape.models import Security, AssetClass, Country, Currency, Industry, Exchange, Tag

# uri = 'sqlite:///databases/TickerScrape.db'
# uri = 'sqlite:///fidash/databases/TickerScrape.db'

def get_db_path(relpath):
    """
    Need 4 /'s to specify absolute path for sqlalchemy
    e.g. sqlite:////fidash/databases/TickerScrape.db
    Need 3 /'s for relative paths
    relpath has 3 /'s
    """
    package_dir = os.path.abspath(os.path.dirname(__file__))
    db_dir = os.path.join(package_dir, relpath)
    uri = ''.join(['sqlite:///', db_dir])
    print (uri)
    return uri

uri = get_db_path('databases/TickerScrape.db')


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


