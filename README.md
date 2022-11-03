# Experiment Reporting Python Package

## Installation
Clone the repository and use pip to build the package locally. For example if the repo is in '~Documents/carbon_tracker'

`
$ pip install ~/Documents/carbon_tracker
`

## Usage
The package will check if it can access the intel-rapl directory and use the values here for
calculating joules otherwise it will use the [python-energy-monitor](https://github.com/mattclifford1/python-energy-monitor) package 

```
import carbon_tracker

tracker = carbon_tracker.Tracker()
tracker.start()
// code goes here
tracker.stop()
```
Args:
 - log_filepath (str): Filepath to csv file to log results. Default: './experiment_log.csv'
 - country (str): Country for estimating gCO2e per kWh Default: 'United Kingdom'


## Carbon Calculation
To estimate the co2e value the tracker uses the carbon intensity for the given country and uses the corresponding gco2/kWh value from here https://ourworldindata.org/grapher/carbon-intensity-electricity
The default value is United Kingdom. 