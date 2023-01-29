"""
This module used to  generate the Below Report

For every year, for every weather station, calculate:

* Average maximum temperature (in degrees Celsius)
* Average minimum temperature (in degrees Celsius)
* Total accumulated precipitation (in centimeters)

Ignore missing data when calculating these statistics.

Design a new data model to store the results. Use NULL for statistics that cannot be calculated.

Your answer should include the new model definition as well as the code used to calculate the new values and store them in the database.

Author: Divya M

"""
import pandas as pd

from data_model import WeatherDataModel, WeatherStatsDataModel

# Creating the instance of Weather DataModel
weather_data_model = WeatherDataModel()
weather_stats_data_model = WeatherStatsDataModel()
import numpy as np


def generate_report():
    """
    This function generates the aggregation report

    For every year, for every weather station, calculate:
        * Average maximum temperature (in degrees Celsius)
        * Average minimum temperature (in degrees Celsius)
        * Total accumulated precipitation (in centimeters)

    And dumps the data into WeatherStats table  using new Data model
    :return:
    """
    weather_data = weather_data_model.get_data()

    # Creating  the year field
    weather_data['Year'] = weather_data['Date'].str[:4]

    # filter for NULL values
    weather_data = weather_data[
        (weather_data['Date'] != -9999) & (weather_data['MaxTemp'] != -9999) & (weather_data['MinTemp'] != -9999) & (
                    weather_data['Precipitation'] != -9999)]

    report = weather_data.groupby([ 'StationID','Year']).agg(
        {'MaxTemp': np.mean, 'MinTemp': np.mean, 'Precipitation': sum}).reset_index()
    # converting tenths of Celsius to Celsius
    report[['MaxTemp','MinTemp']] = round(report[['MaxTemp','MinTemp']]/10,2)
    # converting tenths of  mm into cm
    report[['Precipitation']] = round(report[['Precipitation']]/100,2)

    # Inserting data  into sqlite record by record
    for index, record in report.iterrows():
        print(weather_stats_data_model.add_entry(tuple(record)))


if __name__ == '__main__':
    generate_report()
