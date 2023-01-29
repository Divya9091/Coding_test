"""
The wx_data directory has files containing weather data records from 1985-01-01 to 2014-12-31.
    Each file corresponds to a particular weather station from Nebraska, Iowa, Illinois, Indiana, or Ohio.

Each line in the file contains 4 records separated by tabs:

1. The date (YYYYMMDD format)
2. The maximum temperature for that day (in tenths of a degree Celsius)
3. The minimum temperature for that day (in tenths of a degree Celsius)
4. The amount of precipitation for that day (in tenths of a millimeter)

Missing values are indicated by the value -9999.

Problem 1 - Data Modeling
-------------------------
Choose a database to use for this coding exercise (SQLite, Postgres, etc.).
 Design a data model to represent the weather data records.
 If you use an ORM, your answer should be in the form of that ORM's data definition format.
 If you use pure SQL, your answer should be in the form of DDL statements.

Problem 2 - Ingestion
---------------------
Write code to ingest the weather data from the raw text files supplied into your database,
 using the model you designed. Check for duplicates: if your code is run twice,
 you should not end up with multiple rows with the same data in your database.
 Your code should also produce log output indicating start and end times and number of records ingested.

Author: Divya M
"""

import os
import pandas as pd
import datetime
from data_model import WeatherDataModel

# Creating the instance of DataModel
datamodel = WeatherDataModel()


def data_ingestion():
    """
    This function ingests wx data into SQLite data
    :return:
    """
    print(f'Start Time:{datetime.datetime.now()}')
    # Listing out all the  files from WX data  folder to ingest them into SQLite DB
    files = os.listdir('../wx_data')
    counter = 0  # counter to indicate no of unique records inserted into DB
    for filename in files:
        # Reading the tab seperated file using pandas library
        data = pd.read_csv(f'../wx_data/{filename}', sep='\t', header=None,
                           names=['Date', 'MaxTemp', 'MinTemp', 'Precipitation'])
        # filling missing values  with  -9999
        data.fillna(-9999)
        # Adding  stationid field into dataframe with File name
        data['StationID'] = filename.replace('.txt', '')
        data = data[['StationID', 'Date', 'MaxTemp', 'MinTemp', 'Precipitation']]

        # dropping duplicates if any
        data.drop_duplicates(subset=['Date'], inplace=True)

        # Inserting data  into sqlite record by record
        for index, record in data.iterrows():
            counter += datamodel.add_entry(tuple(record))

    print(f'End Time:{datetime.datetime.now()}')
    print('Total Records inserted: ', counter)


if __name__ == '__main__':
    data_ingestion()
