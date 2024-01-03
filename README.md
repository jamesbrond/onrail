# OnRail

![GitHub top language](https://img.shields.io/github/languages/top/jamesbrond/onrail?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues-raw/jamesbrond/onrail)

## Installation

    python -m venv venv

    source ./venv/Script/activate

    pip install -r requirements.txt

## Usage

    python onrail.py [options]


    -h, --help            show help message and exit
    --version             show program's version number and exit
    -c CONFIG, --config CONFIG
                          Use the YAML configuration file
    -v, --verbose         Produce a more verbose output
    --debug               Writes debug information to onrail.log file
    -s --start START      Start period date (default today)
    -e --end END          End period date. Default end of start date month
    --calendar            Show calendar
