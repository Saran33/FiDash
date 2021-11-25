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

# manually force push to remote
git push -f https://github.com/PWE-Capital/FiDash


# Check repo size:
curl -s https://github.com/Saran33/FiDash | jq '.size' | numfmt --to=iec --from-unit=1024

# Deploy on Heroku
### Install Heroku CLI locally
#### macOS
`brew tap heroku/brew && brew install heroku`
#### Windows
https://devcenter.heroku.com/articles/heroku-cli

### Make Github Repo
Create requirements.txt:
`pip freeze > requirements.txt`
In new dir:
Clone repo:
`git clone https://github.com/PWE-Capital/FiDash`
`cd FiDash`
- Add Procfile:
```zzh
web: gunicorn index:server
```
- Add gitignore:
```zzh
# Heroku
*.pyc
.DS_Store
```

### Set up Heroku
`heroku --version`
`heroku login`
`git init`
`heroku git:remote -a pwemarkets`
`git add .`
`git commit -am "make it better"`
`git push heroku master`