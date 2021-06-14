import time
from Mcp import Mcp

mcp = Mcp(0, 0)


class AirQualitySensor:
    def __init__(self, channel=0):
        self.channel = channel
        self.channel_value = 0

    def read_channel(self):
        value_of_sensor = mcp.read_channel(0)
        return value_of_sensor

    @staticmethod
    def check_quality(value):
        if value > 100:
            return True
        else:
            return False

    @staticmethod
    def closeAirSensor():
        mcp.closespi()
