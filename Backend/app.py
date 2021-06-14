from os import truncate
from flask import json
from flask_cors.core import serialize_option
from repositories.DataRepository import DataRepository
import time
from datetime import datetime
from RPi import GPIO
from Klasses.AirQualitySensor import AirQualitySensor
from Klasses.I2C_LCD import LCD
from subprocess import check_output
import threading
from datetime import datetime
import serial
import logging

import flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request


# code voor de Hardware
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Temperature Sensor Information
temp_sensor_file_name = '/sys/bus/w1/devices/28-012022476e8d/w1_slave'
temperature = 0

# Air Quality Sensor Information
airsensor = AirQualitySensor()
air_quality = 0
air_quality_meaning = "Good"

# Seriele poort informatie
ser = serial.Serial('/dev/ttyS0', 9600, timeout=2)
ser.flush()
sending = False

# LCD Informatie
lcd = LCD()
lcd.backlight(1)


def get_ipadress():
    time.sleep(5)
    ips = check_output(["hostname", "--all-ip-address"])
    ips = ips.decode()
    print(ips)
    ip_adresses_1 = ips[0:ips.find(' ')]
    while len(ip_adresses_1) > 16:
        get_ipadress()
    return ip_adresses_1


# ip_adresses_2 = ips[ips.find(' ') + 1:]
# if len(ip_adresses_2) > 16:
#     ip_adresses_2 = ip_adresses_2[0:ips.find(' ')-2]
# if len(ip_adresses_2) < 16:
#     ip_adresses_2 = ""
lcd.lcd_clear()
lcd.lcd_display_string("SEB By Brooklyn")
lcd.lcd_display_string(get_ipadress(), 2)

# Verbruik
verbruik = 0
verbruik_now = 0

# Code voor flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretKeyBrooklyn'
socketio = SocketIO(app, cors_allowed_origins="*",
                    logger=False, engineio_logger=True, ping_timeout=1)
CORS(app)


# Threading Points   : Code nog op te ruimen
def datalogger():
    while True:
        global temperature
        global air_quality
        global air_quality_meaning
        global verbruik
        global verbruik_now
        global sending

        # temp opvragen
        sensor_file = open(temp_sensor_file_name, 'r')
        for i, line in enumerate(sensor_file):
            if i == 1:
                temperature_now = int(line.strip(
                    '\n')[line.find('t=')+2:])/1000.0
        sensor_file.close()

        if temperature_now != temperature:
            socketio.emit('B2F_information_temp', {
                          'temp': round(temperature_now, 2)})
            temperature = temperature_now

        # AirQuality Opvragen
        air_quality_now = airsensor.read_channel()
        if air_quality != air_quality_now:
            if air_quality_now > 700 and air_quality_meaning != "Danger":
                air_quality_meaning = "Danger"
                air_quality = air_quality_now
            elif air_quality_now > 300 and air_quality_meaning != "Not Good":
                air_quality_meaning = "Not Good"
                air_quality = air_quality_now
            elif air_quality_now <= 300 and air_quality_meaning != "Good":
                air_quality_meaning = "Good"
                air_quality = air_quality_now
            print(air_quality_meaning)
            socketio.emit('B2F_information_air_quality', {
                'air_quality': air_quality_meaning, })

        # Verbuik Opvragen
        if sending == True:
            time.sleep(1)
        try:
            if sending != True:
                sending = True
                string = "Verbruik"
                ser.write(string.encode())
                b = ser.readline()
                print(f"De waarde van port: {b}")
                string_n = b.decode('utf-8', errors="ignore").rstrip()
                print(f"De waarde is: {string_n}")
                if string_n[0:8] == "Verbruik":
                    if string_n[9:] != "":
                        if len(string_n) < 17:
                            verbruik_now = float(string_n[9:])
                            if verbruik_now != verbruik:
                                socketio.emit('B2F_information_verbruik', {
                                    'verbruik': round(verbruik_now)})
                                verbruik = verbruik_now
                sending = False
        except:
            print(f"Er is iets fout gelopen")
            logging.info("Er is iets fout gelopen")

        print(f"\n------------Information------------")
        print(f"Temperature is: {temperature} °C")
        print(f"Air quality is: {air_quality_now}")
        print(f"Het verbruik is: {verbruik} W")

        # 3: Luchtkwaliteit inlezen (actie)
        # 4: Verbruik inlezen (actie)
        # 5: Temp inlezen (actie)

        # 1: Air Quality Sensor (Sensor)
        # 2: Temperature Sensor (Sensor)
        # 3: Current Sensor (Sensor)

        # Luchtkwaliteit doorsturen naar db
        tijd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(tijd)
        DataRepository.insert_historiek(
            tijd, round(float(air_quality_now), 2), "luchtkwaliteit", 1, 5)
        # Temp doorsturen naar db
        DataRepository.insert_historiek(
            tijd, round(float(temperature), 2), "temperatuur", 2, 3)
        # Verbruik doorsturen naar db
        if verbruik != 0:
            DataRepository.insert_historiek(
                tijd, verbruik, "Verbruik", 3, 4)
        time.sleep(7)


def logger_drukknoppen():
    while True:
        actie_id = 0
        b = ""
        string_n = ""
        while ser.inWaiting():
            b = ser.readline()
            string_n = b.decode().rstrip()
            print(string_n)
        if string_n[0:4] == "Knop":
            if string_n[4:5] == "1":
                new_status = int(string_n[6:7])
                status_stopcontact_now = DataRepository.read_status_relay_by_id(1)[
                    "status_actuator"]
                tijd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if status_stopcontact_now != new_status:
                    if new_status == 1:
                        actie_id = 1
                    else:
                        actie_id = 2
                res = DataRepository.insert_status_relay(
                    tijd, new_status, 1, actie_id)
                socketio.emit('B2F_verandering_stopcontact', {
                    'relayid': 1, "relaystatus": new_status})
            if string_n[4:5] == "2":
                new_status = int(string_n[6:7])
                status_stopcontact_now = DataRepository.read_status_relay_by_id(2)[
                    "status_actuator"]
                tijd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if status_stopcontact_now != new_status:
                    if new_status == 1:
                        actie_id = 1
                    else:
                        actie_id = 2
                res = DataRepository.insert_status_relay(
                    tijd, new_status, 2, actie_id)
                socketio.emit('B2F_verandering_stopcontact', {
                    'relayid': 2, "relaystatus": new_status})
            if string_n[4:5] == "3":
                new_status = int(string_n[6:7])
                status_stopcontact_now = DataRepository.read_status_relay_by_id(3)[
                    "status_actuator"]
                tijd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if status_stopcontact_now != new_status:
                    if new_status == 1:
                        actie_id = 1
                    else:
                        actie_id = 2
                res = DataRepository.insert_status_relay(
                    tijd, new_status, 3, actie_id)
                socketio.emit('B2F_verandering_stopcontact', {
                    'relayid': 3, "relaystatus": new_status})
            if string_n[4:5] == "4":
                new_status = int(string_n[6:7])
                status_stopcontact_now = DataRepository.read_status_relay_by_id(4)[
                    "status_actuator"]
                tijd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if status_stopcontact_now != new_status:
                    if new_status == 1:
                        actie_id = 1
                    else:
                        actie_id = 2
                res = DataRepository.insert_status_relay(
                    tijd, new_status, 4, actie_id)
                socketio.emit('B2F_verandering_stopcontact', {
                    'relayid': 4, "relaystatus": new_status})
            if string_n[4:5] == "5":
                new_status = int(string_n[6:7])
                status_stopcontact_now = DataRepository.read_status_relay_by_id(5)[
                    "status_actuator"]
                tijd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if status_stopcontact_now != new_status:
                    if new_status == 1:
                        actie_id = 1
                    else:
                        actie_id = 2
                res = DataRepository.insert_status_relay(
                    tijd, new_status, 5, actie_id)
                socketio.emit('B2F_verandering_stopcontact', {
                    'relayid': 5, "relaystatus": new_status})
            if string_n[4:5] == "6":
                new_status = int(string_n[6:7])
                status_stopcontact_now = DataRepository.read_status_relay_by_id(6)[
                    "status_actuator"]
                tijd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if status_stopcontact_now != new_status:
                    if new_status == 1:
                        actie_id = 1
                    else:
                        actie_id = 2
                res = DataRepository.insert_status_relay(
                    tijd, new_status, 6, actie_id)
                socketio.emit('B2F_verandering_stopcontact', {
                    'relayid': 6, "relaystatus": new_status})
            if string_n[4:5] == "7":
                new_status = int(string_n[6: 7])
                status_stopcontact_now = DataRepository.read_status_relay_by_id(7)[
                    "status_actuator"]
                tijd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if status_stopcontact_now != new_status:
                    if new_status == 1:
                        actie_id = 1
                    else:
                        actie_id = 2
                res = DataRepository.insert_status_relay(
                    tijd, new_status, 7, actie_id)
                socketio.emit('B2F_verandering_stopcontact', {
                    'relayid': 7, "relaystatus": new_status})
            if string_n[4:5] == "8":
                new_status = int(string_n[6: 7])
                status_stopcontact_now = DataRepository.read_status_relay_by_id(8)[
                    "status_actuator"]
                tijd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if status_stopcontact_now != new_status:
                    if new_status == 1:
                        actie_id = 1
                    else:
                        actie_id = 2
                res = DataRepository.insert_status_relay(
                    tijd, new_status, 8, actie_id)
                socketio.emit('B2F_verandering_stopcontact', {
                    'relayid': 8, "relaystatus": new_status})
        time.sleep(1)


thread = threading.Timer(9, datalogger)
thread2 = threading.Timer(1, logger_drukknoppen)
thread.start()
thread2.start()


print("**** Program Started ****")

# API endpoints

endpoint = "/api/v1"


@ app.route(endpoint + '/')
def hallo():
    return "Server is running"


@ app.route(endpoint + '/historiek/<id>', methods=['GET'])
def historiek(id):
    if request.method == 'GET':
        # 1: luchtkwaliteit, 2: temperatuur, 3: currentsensor
        data = DataRepository.read_historiek_by_sensor_id(id)
        if data is not None:
            return jsonify(data), 200
        else:
            return jsonify(message='error'), 404


@ app.route(endpoint + "/historiek_last_day/<id>", methods=['GET'])
def historiek_last_24_hours(id):
    if request.method == 'GET':
        data = DataRepository.read_historiek_last_24_hours_every_hour(id)
        if data is not None:
            return jsonify(data), 200
        else:
            return jsonify(message='error'), 404


@ app.route(endpoint + "/historiek_time/<id>/<starttime>/<stoptime>", methods=['GET'])
def historiek_time(id, starttime, stoptime):
    if request.method == 'GET':
        start_time = datetime.strptime(starttime, '%Y-%m-%dT%H:%M')
        start_time = datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')
        stop_time = datetime.strptime(stoptime, '%Y-%m-%dT%H:%M')
        stop_time = datetime.strftime(stop_time, '%Y-%m-%d %H:%M:%S')
        data = DataRepository.read_historiek_by_date(id, start_time, stop_time)
    return jsonify(data)


@ app.route(endpoint + '/read_temperature', methods=['GET'])
def read_temperature():
    sensor_file = open(temp_sensor_file_name, 'r')
    for i, line in enumerate(sensor_file):
        if i == 1:
            temperature = int(line.strip('\n')[line.find('t=')+2:])/1000.0
    sensor_file.close()
    return jsonify(temp=round(temperature, 2))


@ app.route(endpoint + '/read_verbruik', methods=['GET'])
def read_verbruik():
    data = DataRepository.read_historiek_by_sensor_id_last(3)
    return jsonify(verbruik=data)


@ app.route(endpoint + '/read_airquality', methods=['GET'])
def read_airquality():
    air_quality = airsensor.read_channel()
    string_for_air_quality = ""

    if air_quality > 700:
        string_for_air_quality = "Danger"
    elif air_quality > 300:
        string_for_air_quality = "Not Good"
    else:
        string_for_air_quality = "Good"

    return jsonify(air_quality=string_for_air_quality)


@ app.route(endpoint + '/read_stopcontacten', methods=['GET'])
def read_stopcontacten():
    if request.method == 'GET':
        data = DataRepository.read_status_relays()
        if data is not None:
            return jsonify(data), 200
        else:
            return jsonify(message='error'), 404


@ socketio.on('F2B_switch_stopcontact')
def switch_stopcontact(data):
    global sending
    tijd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    relay_id = data['relay_id']
    new_status = data['new_status']
    print(f"stopcontact {relay_id} wordt geswitcht naar {new_status}")
    if new_status == 1:
        actie_id = 1
    else:
        actie_id = 2
    res = DataRepository.insert_status_relay(
        tijd, new_status, relay_id, actie_id)

    data = DataRepository.read_status_relay_by_id(relay_id)
    print(data["status_actuator"], data["actuatorId"])
    socketio.emit('B2F_verandering_stopcontact', {
                  'relayid': data["actuatorId"], "relaystatus": data["status_actuator"]})

    if new_status == 1:
        string_state = "Aan"
    else:
        string_state = "Uit"
    string = "Knop" + relay_id + string_state
    print(string.encode())

    if sending == True:
        time.sleep(1)

    if sending != True:
        sending = True
        ser.write(string.encode())
        b = ser.readline()
        string_n = b.decode().rstrip()
        print(string_n)
        if string_n != "Ok":
            time.sleep(0.5)
            ser.write(string.encode())
        sending = False


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
