Preview markup in VS code with:
cmd + k + v
or
ctrl + k + v

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

### Run locally with Gunicorn
`gunicorn fidash_app:server -b :8000`

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
`git commit -am "Update"`
`git push heroku main`
`heroku ps:scale web=1`

### Restart dynos
`heroku ps:restart web`

### Check for errors
`heroku logs --tail`
### Open the app in browser
`heroku open`
### Provision a Dyno container with a bash shell
`heroku run bash -a pwemarkets`

### View Free Dyno Hours
`heroku ps -a pwemarkets`

To switch the default branch used to deploy apps from master to main:
https://help.heroku.com/O0EXQZTA/how-do-i-switch-branches-from-master-to-main
`git checkout -b main`
`git branch -D master`
https://github.com/heroku/heroku-repo#reset
`heroku repo:reset -a pwemarkets`
`git push heroku main`

### RUN GUNICORN WITHOUT ASYNC
Add to procfile:
heroku web: gunicorn -w 1 :app --preload

### Set Secret Key for cookie encryption
`heroku config:set SECRET_KEY="YOUR_SECRET_KEY_VALUE"`