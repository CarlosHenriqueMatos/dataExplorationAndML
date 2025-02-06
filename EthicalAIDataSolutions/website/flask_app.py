from flask import Flask
from flask import render_template, request, jsonify
import os
import pickle
import pandas as pd
import joblib

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))     
# set file directory path
MODEL_PATH = os.path.join(APP_ROOT, "./model.pkl")  
# set path to the model

# if this path doesnt work, try to replace the string with MODEL_PATH
loaded_model = joblib.load("./model.pkl")
print("bruh",type(loaded_model))

"""
with open("./model.pkl", "rb") as f:
    loaded_model = pickle.load(f)
    print("bruh",type(loaded_model))"""

list_of_all_keys = ["HourlySkyConditions", "HourlyVisibility",
                    "HourlyPresentWeatherType", "HourlyDryBulbTemperatureC",
                    "HourlyWetBulbTemperatureC", "HourlyDewPointTemperatureC",
                    "HourlyRelativeHumidity", "HourlyWindSpeed","HourlyWindDirection",
                    "HourlyWindGustSpeed", "HourlyStationPressure",
                    "HourlyPressureTendency","HourlyPressureChange",
                    "HourlySeaLevelPressure","HourlyPrecipitation",
                    "HourlyAltimeterSetting","DailyAverageDryBulbTemperature",
                    "DailyDepartureFromNormalAverageTemperature",
                    "DailyAverageRelativeHumidity","DailyAverageWetBulbTemperature",
                    "DailySunrise","DailySunset","DailyPrecipitation","DailySnowfall",
                    "DailySnowDepth","DailyAverageStationPressure",
                    "DailyAverageSeaLevelPressure","DailyAverageWindSpeed",
                    "DailyPeakWindSpeed","PeakWindDirection",
                    "DailySustainedWindSpeed","DailySustainedWindDirection"]

data_to_be_given_to_model = {'ELEVATION': [201.8], 
                             'LATITUDE': [41.995], 'LONGITUDE': [-87.9336], 'HourlySkyConditions': [120.0], 'HourlyVisibility': [10.0], 'HourlyPresentWeatherType': [0.0], 'HourlyDryBulbTemperatureF': [31.0], 'HourlyDryBulbTemperatureC': [0.0], 'HourlyWetBulbTemperatureF': [28.0], 'HourlyWetBulbTemperatureC': [-1.5], 'HourlyDewPointTemperatureF': [18.0], 'HourlyDewPointTemperatureC': [-6.7], 'HourlyRelativeHumidity': [61.0], 'HourlyWindSpeed': [10.0], 'HourlyWindDirection': [15.0], 'HourlyWindGustSpeed': [0.0], 'HourlyStationPressure': [29.32], 'HourlyPressureTendency': [0.0], 'HourlyPressureChange': [0.0], 'HourlySeaLevelPressure': [38.0], 'HourlyPrecipitation': [0.0], 'HourlyAltimeterSetting': [30.04], 'DailyMaximumDryBulbTemperature': [0.0], 'DailyMinimumDryBulbTemperature': [0.0], 'DailyAverageDryBulbTemperature': [0.0], 'DailyDepartureFromNormalAverageTemperature': [0.0], 'DailyAverageRelativeHumidity': [0.0], 'DailyAverageDewPointTemperature': [0.0], 'DailyAverageWetBulbTemperature': [0.0], 'DailyCoolingDegreeDays': [0.0], 'DailySunrise': [1202.0], 'DailySunset': [2342.0], 'DailyPrecipitation': [0.0], 'DailySnowfall': [0.0], 'DailySnowDepth': [0.0], 'DailyAverageStationPressure': [0.0], 'DailyAverageSeaLevelPressure': [0.0], 'DailyAverageWindSpeed': [0.0], 'DailyPeakWindSpeed': [0.0], 'PeakWindDirection': [0.0], 'DailySustainedWindSpeed': [0.0], 'DailySustainedWindDirection': [0.0], 'MonthlyMaximumTemperature': [0.0], 'MonthlyMinimumTemperature': [0.0], 'MonthlyMeanTemperature': [0.0], 'MonthlyAverageRH': [0.0], 'MonthlyDewpointTemperature': [0.0], 'MonthlyWetBulb': [0.0], 'MonthlyHeatingDegreeDays': [0.0], 'MonthlyCoolingDegreeDays': [0.0], 'MonthlyStationPressure': [0.0], 'MonthlySeaLevelPressure': [0.0], 'MonthlyAverageWindSpeed': [0.0], 'MonthlyTotalSnowfall': [0.0], 'MonthlyDepartureFromNormalMaximumTemperature': [0.0], 'MonthlyDepartureFromNormalMinimumTemperature': [0.0], 'MonthlyDepartureFromNormalAverageTemperature': [0.0], 'MonthlyDepartureFromNormalPrecipitation': [0.0], 'MonthlyTotalLiquidPrecipitation': [0.0], 'MonthlyGreatestPrecip': [0.0], 'MonthlyGreatestPrecipDate': [0.0], 'MonthlyGreatestSnowfall': [0.0], 'MonthlyGreatestSnowfallDate': [0.0], 'MonthlyGreatestSnowDepth': [0.0], 'MonthlyGreatestSnowDepthDate': [0.0], 'MonthlyDaysWithGT90Temp': [0.0], 'MonthlyDaysWithLT32Temp': [0.0], 'MonthlyDaysWithGT32Temp': [0.0], 'MonthlyDaysWithLT0Temp': [0.0], 'MonthlyDaysWithGT001Precip': [0.0], 'MonthlyDaysWithGT010Precip': [0.0], 'MonthlyMaxSeaLevelPressureValue': [0.0], 'MonthlyMaxSeaLevelPressureValueDate': [0.0], 'MonthlyMaxSeaLevelPressureValueTime': [0.0], 'MonthlyMinSeaLevelPressureValue': [0.0], 'MonthlyMinSeaLevelPressureValueDate': [0.0], 'MonthlyMinSeaLevelPressureValueTime': [0.0], 'MonthlyTotalHeatingDegreeDays': [0.0], 'MonthlyTotalCoolingDegreeDays': [0.0], 'MonthlyDepartureFromNormalHeatingDD': [0.0], 'MonthlyDepartureFromNormalCoolingDD': [0.0]}

@app.route("/")
def hello_world():
    return render_template('decision_tree_integration.html')


@app.route("/process", methods=["POST"])
def process():
    data = request.json
    values_list = data["values_list"]
    model_data_dict = dict()
    key_iterator_counter = 0
    while (key_iterator_counter < len(list_of_all_keys)):
        model_data_dict[list_of_all_keys[key_iterator_counter]] = [values_list[key_iterator_counter]]
        key_iterator_counter += 1
    for key in list(model_data_dict.keys()):
        data_to_be_given_to_model[key] = model_data_dict[key]
    model_data = pd.DataFrame(data_to_be_given_to_model)
    model_data.to_csv("./user_data.csv",index=False)
    # print(model_data)
    predicted_value = loaded_model.predict(model_data)
    return jsonify({"data":str(predicted_value[0])})

if __name__ == "__main__":
    app.run(debug=True)
