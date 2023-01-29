import requests
import unittest


class SimpleTest(unittest.TestCase):

    # Returns True or False.
    def test_stats_success(self):
        response = requests.get('http://10.0.0.20:5000//api/weather/stats?date=19850102&stationid=USC00116526').json()
        self.assertTrue(len(response))

    # Returns True or False.
    def test_stats_failure(self):
        response = requests.get('http://10.0.0.20:5000//api/weather/stats?date=19850102&stationi=USC00116526').json()
        self.assertTrue('Failure' in response['status'])

    # Returns True or False.
    def test_weather_raw_data_success(self):
        response = requests.get('http://10.0.0.20:5000//api/weather?date=19850102&stationid=USC00116526').json()
        self.assertTrue(len(response))

    # Returns True or False.
    def test_weather_raw_data_failure(self):
        response = requests.get('http://10.0.0.20:5000//api/weather?dat=19850102&stationi=USC00116526').json()
        self.assertTrue('Failure' in response['status'])


if __name__ == '__main__':
    unittest.main()