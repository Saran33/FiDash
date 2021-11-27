from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='fidash',
    packages=find_packages(include=['fidash']),
    version='0.22',
    author='Saran Connolly',
    description='PWE Capital Finance dashboard.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PWE-Capital/fidash",
    project_urls={
        "Bug Tracker": "https://github.com/PWE-Capital/fidash/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pwe @ git+https://github.com/Saran33/pwe_analysis',
        'TickerScrape @ git+git://github.com/Saran33/TickerScrape.git',
        'pandas-datareader', 'dash', 'dash-datetimepicker',  # 'yahoo_fin', 'yfinance',
        'dash-bootstrap-components', 'SQLAlchemy', 'networkx',  # 'matplotlib', 'seaborn',
        'pykalman', 'Flask-SQLAlchemy', 'gunicorn',
        'Flask-Login @ git+git://github.com/maxcountryman/flask-login',

    ],
    #package_dir={"": "src"},
    # packages=find_packages(where="fidash"),
    python_requires="==3.8.11",
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
