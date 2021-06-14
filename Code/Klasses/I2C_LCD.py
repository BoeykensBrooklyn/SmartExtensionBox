import time
import smbus

address = 0x20


class PCF8574A:
    def __init__(self, address, port=1):
        self.address = address
        self.bus = smbus.SMBus(port)

    def write_cmd(self, cmd):
        self.bus.write_byte(self.address, cmd)
        time.sleep(0.0001)

    def write_cmd_arg(self, cmd, data):
        self.bus.write_byte_data(self.address, cmd, data)
        time.sleep(0.0001)

    def write_block_data(self, cmd, data):
        self.bus.write_block_data(self.address, cmd, data)
        time.sleep(0.0001)

    def read(self):
        return self.bus.read_byte(self.address)

    def read_data(self, cmd):
        return self.bus.read_byte_data(self.address, cmd)

    def read_block_data(self, cmd):
        return self.bus.read_block_data(self.address, cmd)


class LCD:
    def __init__(self):
        self.lcd_device = PCF8574A(address)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x02)
        self.lcd_write(0x20 | 0x08 |
                       0x00 | 0x00)
        self.lcd_write(0x08 | 0x04)
        self.lcd_write(0x01)
        self.lcd_write(0x04 | 0x02)
        time.sleep(0.2)

    def lcd_strobe(self, data):
        self.lcd_device.write_cmd(data | 0b00000100 | 0x08)
        time.sleep(.0005)
        self.lcd_device.write_cmd(((data & ~0b00000100) | 0x08))
        time.sleep(.0001)

    def lcd_write_four_bits(self, data):
        self.lcd_device.write_cmd(data | 0x08)
        self.lcd_strobe(data)

    # write a command to lcd
    def lcd_write(self, cmd, mode=0):
        self.lcd_write_four_bits(mode | (cmd & 0xF0))
        self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

    # write a character to lcd (or character rom) 0x09: backlight | RS=DR<
    # works!
    def lcd_write_char(self, charvalue, mode=1):
        self.lcd_write_four_bits(mode | (charvalue & 0xF0))
        self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))

    # put string function with optional char positioning
    def lcd_display_string(self, string, line=1, pos=0):
        if line == 1:
            pos_new = pos
        elif line == 2:
            pos_new = 0x40 + pos
        elif line == 3:
            pos_new = 0x14 + pos
        elif line == 4:
            pos_new = 0x54 + pos

        self.lcd_write(0x80 + pos_new)

        for char in string:
            self.lcd_write(ord(char), 0b00000001)

    # clear lcd and set to home
    def lcd_clear(self):
        self.lcd_write(0x01)
        self.lcd_write(0x02)

    # define backlight on/off (lcd.backlight(1); off= lcd.backlight(0)
    def backlight(self, state):  # for state, 1 = on, 0 = off
        if state == 1:
            self.lcd_device.write_cmd(0x08)
        elif state == 0:
            self.lcd_device.write_cmd(0x00)

    # add custom characters (0 - 7)
    def lcd_load_custom_chars(self, fontdata):
        self.lcd_write(0x40)
        for char in fontdata:
            for line in char:
                self.lcd_write_char(line)
