# from typing_extensions import ParamSpec
from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

# relays

    @staticmethod
    def read_status_relays():
        sql = "SELECT h.actuatorId, h.Datum, h.status_actuator FROM historiek as h WHERE Datum = (SELECT MAX(Datum) FROM historiek WHERE actuatorId = h.actuatorId GROUP BY actuatorId) order by actuatorId"
        return Database.get_rows(sql)

    @staticmethod
    def read_status_relay_by_id(id):
        sql = "SELECT historiekId, datum, status_actuator, commentaar, actuatorId, actieId  from historiek WHERE actuatorId = %s ORDER BY Datum DESC LIMIT 1;"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def insert_status_relay(datum, status, actuatorid, actieId):
        sql = "INSERT INTO historiek (datum, status_actuator, actuatorId, actieId) VALUES (%s, %s, %s, %s)"
        params = [datum, status, actuatorid, actieId]
        return Database.execute_sql(sql, params)

# historiek sensors
    @staticmethod
    def read_historiek():
        sql = "SELECT * from historiek"
        return Database.get_rows(sql)

    @staticmethod
    def read_historiek_by_sensor_id(id):
        sql = "SELECT * from historiek WHERE sensorId = %s"
        params = [id]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_historiek_by_sensor_id_last(id):
        sql = "SELECT * from historiek WHERE sensorId = %s ORDER BY Datum DESC LIMIT 1;"
        params = [id]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_historiek_last_24_hours(id):
        sql = "SELECT * FROM historiek WHERE sensorId = %s AND datum >= NOW() - INTERVAL 1 DAY"
        params = [id]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_historiek_last_24_hours_every_hour(id):
        sql = "SELECT * FROM historiek WHERE sensorId = %s AND datum >= NOW() - INTERVAL 1 DAY GROUP BY DATE(datum), HOUR(datum)"
        params = [id]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_historiek_by_date(id, startdate, enddate):
        sql = "SELECT * FROM historiek WHERE sensorId = %s AND datum between %s and %s"
        Params = [id, startdate, enddate]
        return Database.get_rows(sql, Params)

    @staticmethod
    def insert_historiek(datum, value, commentaar, sensorid, actieId):
        sql = "INSERT INTO historiek (datum, waarde_sensor, commentaar, sensorId, actieId) VALUES (%s, %s, %s, %s, %s)"
        params = [datum, value, commentaar, sensorid, actieId]
        return Database.execute_sql(sql, params)
