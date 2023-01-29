from flask import Flask, request, Response, jsonify
from data_model import WeatherDataModel, WeatherStatsDataModel
from flasgger import Swagger, swag_from

app = Flask(__name__)

swagger = Swagger(app)

@app.route("/")
def home():
    return "Weather App"


def pagination(data, start, limit):
    if len(data) > start:
        return data[start:start + limit]
    else:
        return data


@app.route("/api/weather", methods=['GET'])
def weather():
    """Example endpoint returning a list of weather data  for specific stationid and date
        ---
        parameters:
          - date: string
            stationid: string
            start: optional
            limit: optional
        responses:
          200:
            description: A list of weather data for  filter stationid and date
            schema:
              Date: date,
              MaxTemp: The maximum temperature for that day (in tenths of a degree Celsius),
              MinTemp: The minimum temperature for that day (in tenths of a degree Celsius),
              Precipitation: The minimum temperature for that day (in tenths of a degree Celsius),
              StationID: input stationid
            examples:
              {
                  "limit": 20,
                  "results": [
                    {
                      "Date": "19850102",
                      "MaxTemp": -33,
                      "MinTemp": -183,
                      "Precipitation": 0,
                      "StationID": "USC00116526"
                    }
                  ],
                  "start": 0,
                  "status": "ok"
                }
        """
    args = request.args
    date = args.get('date')
    stationid = args.get('stationid')
    start = args.get('start', 0)
    limit = args.get('limit', 20)
    if stationid is None or date is None:
        return jsonify(status='Failure',results='Missing date or stationid parameter')

    weather_dm = WeatherDataModel()
    response = weather_dm.get_data(query=[stationid, date]).to_dict(orient='records')
    return jsonify(status='ok', results=pagination(response, start, limit),start=start,limit=limit)


@app.route("/api/weather/stats", methods=['GET'])
def stats():
    """Example endpoint returning a list of weather stats(aggregated  data)  for specific stationid
        ---
        parameters:
            stationid: string
            start: optional
            limit: optional
        responses:
          200:
            description: A list of weather stats data for filter stationid
            schema:
              Year: year,
              AvgMaxTemp: Average maximum temperature (in degrees Celsius),
              AvgMinTemp: Average minimum temperature (in degrees Celsius),
              Total Precipitation: Total accumulated precipitation (in centimeters),
              StationID: input stationid
            examples:
              {
              "limit": 20,
              "results": [
                {
                  "AvgMaxTemp": 14.56,
                  "AvgMinTemp": 4.06,
                  "StationID": "USC00116526",
                  "TotalPrecipitation": 96.53,
                  "Year": "1985"
                }],
                "start": 0
                }
        """
    args = request.args
    stationid = args.get('stationid')
    start = args.get('start', 0)
    limit = args.get('limit', 20)
    if stationid is None:
        return jsonify(status='Failure',results='Missing year or stationid parameter')

    weatherstats_dm = WeatherStatsDataModel()
    response = weatherstats_dm.get_data(query=[stationid]).to_dict(orient='records')

    return jsonify(status='ok', results=pagination(response, start, limit),start=start,limit=limit)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
