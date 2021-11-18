1. Create venv:
`virtualenv dashenv`
2. Launch venv:
windows:
`./dashenv/scripts/activate`
unix:
`source dashenv/bin/activate`
3. Install Dash and PWE:
`pip install dash`
`pip install dash-bootstrap-components`
`pip install git+git://github.com/Saran33/pwe_analysis.git`
`pip install git+git://github.com/Saran33/TickerScrape`
`pip install pandas-datareader`
`pip install SQLAlchemy`

For dev, when package not installed on server:
`export PYTHONPATH="${PYTHONPATH}:/path/to/your/project/"`

persistence=True — remembers dropdown value. Used with persistence_type
persistence_type='memory'  — remembers dropdown value selected until browser tab is refreshed
persistence_type='session' — until browser tab is closed
persistence_type='local': until browser cookies are deleted