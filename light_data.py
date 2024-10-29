import pandas as pd
from sklearn.externals import joblib
import csv
import json  # library for handling JSON data
# import os.path
import time  # module for sleep operation
from datetime import datetime, date
from boltiot import Bolt

api_key = "ddb39d0e-7a6a-4e4c-803c-82c5fbbb8921"
device_id = "BOLT5436094"
mybolt = Bolt(api_key, device_id)
response1 = mybolt.isOnline()
print(response1)
def get_sensor_value_from_pin(pin):
    """Returns the sensor value. Returns -999 if request fails
    :param pin:
    :return:
    """
    try:
        print('calling')
        response = mybolt.analogReaderror(pin)
        print(response)
        data = json.loads(response)
        if data["success"] != 1:
            print("Request not successfull. This is the response->", data)
            return -999
        sensor_value = int(data["value"])
        return sensor_value
    except Exception as e:
        print("Something went wrong when returning the sensor value")
        print(e)
        return -999
filename = "light_data.csv"
# while True:
sensor_value = get_sensor_value_from_pin("A0")
print("The current sensor value is:", sensor_value)
threshold = 350
# sensor_value = 400
if sensor_value <= threshold:
    response = mybolt.digitalWrite(4, "HIGH")
    ls = 'ON'
else:
    response = mybolt.digitalWrite(4, "LOW")
    ls = 'OFF'
if sensor_value == -999:
    timeML = datetime.now().strftime("%H:%M:%S")
    lin_reg = joblib.load("./HomeAutoML.pkl")

    td = pd.Timedelta(timeML)
    MLlightStatus = int(lin_reg.predict([[td.seconds]]))
    print(MLlightStatus)
    if MLlightStatus == 1:
        response = mybolt.digitalWrite(4, "HIGH")
    else:
        response = mybolt.digitalWrite(4, "LOW")
    # continue

today = date.today().strftime("%m-%d-%Y")
time1 = datetime.now().strftime("%H:%M:%S")
parameters = {'Date': today, 'Time': time1, 'Threshold': threshold, 'SensorValue': sensor_value, 'LightStatus': ls}
with open(filename, 'a', newline='') as file:
    fieldnames = ['Date', 'Time', 'Threshold', 'SensorValue', 'LightStatus']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    # if not os.path.isfile(filename):
    #     writer.writeheader()
    writer.writerow(parameters)
# time.sleep(10)