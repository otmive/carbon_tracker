"""
joules and carbon tracking
usage:
    args:
        - Country (string):     wattage of CPU (thermal design power)
    methods:
        - start()               starts monitoring (automatically called from __init__)
        - stop():                   stops monitoring
    attributes:
        - data (dict):              contains all relevant data collected and estimated
"""

import pandas as pd
import energy_monitor
import os
import datetime
from csv import reader, writer
from carbon_tracker import raplMonitor


class Tracker:
    """
    Args:
        - log_filepath (str): Filepath to csv file to log results. Default: './experiment_log.csv'
        - country (str): Country for estimating gCO2e per kWh Default: 'United Kingdom'
    """
    def __init__(self, country='United Kingdom', log_filepath='./experiment_log.csv'):
        self.country = country
        self.log_filepath = log_filepath
        self.write_data = {}
        self.data = {}
        self.monitor = None
        self.start_time = None
        if os.path.isdir('/sys/class/powercap/intel-rapl:1'):
            self.monitor = raplMonitor.RaplMonitor()
            print("Using rapl")
        else:
            self.monitor = energy_monitor.monitor()
            print("Using energy_monitor")

    def get_carbon_by_country(self):
        # Source https://ourworldindata.org/grapher/carbon-intensity-electricity
        data = pd.read_csv('carbon_tracker/data/carbon-intensity-electricity.csv')
        country = self.country
        # Filter by country
        country_data = data[data.Entity == country]
        # Filter by latest year
        latest_data = country_data.loc[country_data['Year'] == max(country_data['Year'])]

        # Return cCO2/kWh for given country
        return latest_data['Carbon intensity of electricity (gCO2/kWh)'].values[0]

    def start(self):
        self.start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.monitor.start()

    def stop(self):
        self.monitor.stop()
        self.log_data()

    def joules(self):
        return self.monitor.joules

    def co2e(self):
        return self.monitor.joules * 0.0000002778 * self.get_carbon_by_country()  # 1J = 0.0000002778kWh

    def log_data(self):

        self.write_data['date'] = self.start_time
        self.write_data['joules'] = self.joules()
        self.write_data['co2e'] = self.co2e()

        csv_filepath = self.log_filepath
        # if doesn't exist: 'w' else 'a'
        if not os.path.isfile(csv_filepath):
            # make sure directories exist before writing
            os.makedirs(os.path.split(csv_filepath)[0], exist_ok=True)
            with open(csv_filepath, 'w', newline='') as csvfile:
                spamwriter = writer(csvfile, delimiter=',')
                fields = list(self.write_data.keys())
                spamwriter.writerow(fields)
                values = list(self.write_data.values())
                spamwriter.writerow(values)
        else:
            with open(csv_filepath, 'a', newline='') as csvfile:
                spamwriter = writer(csvfile, delimiter=',')
                values = list(self.write_data.values())
                spamwriter.writerow(values)


if __name__ == '__main__':
    pass
