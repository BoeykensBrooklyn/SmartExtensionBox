#pylint: skip-file

import spidev
from RPi import GPIO

volt = 0
percentage = 0
angle = 0


class Mcp:
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 10**5

    def read_channel(self, ch):
        channel = ch << 4 | 128
        bytes_out = [0x01, channel, 0x00]
        bytes_in = self.spi.xfer(bytes_out)
        byte1 = bytes_in[1]
        byte2 = bytes_in[2]
        result = byte1 << 8 | byte2

        if ch == 0:
            return result
        elif ch == 1:
            result = 1023 - result
            return result

    def closespi(self):
        self.spi.close()


def value_to_volt(value):
    volt = round((3.3 * (value / 1023.0)), 2)
    print(f"Pot: Het resultaat is: {volt} V")


def value_to_percentage(value):
    percentage = round(((value / 1023.00) * 100), 2)
    print(f"LDR: Het resultaat is: {percentage} %")


def value_to_angle(value):
    angle = round(((value / 1023.00) * 180), 2)
    return angle


def print_value_to_angle(value):
    angle = round(((value / 1023.00) * 180), 2)
    print(f"LDR: Het resultaat angle is: {angle} °")


def set_servo_motor(value):
    angle_servo = value_to_angle(value)
    duty_cycle = angle_servo/18 + 2
    pwm.start(duty_cycle)
    time.sleep(0.1)


def main():
    set_servo_motor(mcp.read_channel(0))
    time.sleep(0.1)
