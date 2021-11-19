from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='fidash',
    packages=find_packages(include=['fidash']),
    version='0.11',
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
        'yahoo_fin', 'yfinance', 'pandas-datareader', 'dash',
        'dash-bootstrap-components', 'SQLAlchemy', 'matplotlib', 'seaborn', 'networkx',

    ],
    #package_dir={"": "src"},
    # packages=find_packages(where="fidash"),
    python_requires=">=3.8",
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
