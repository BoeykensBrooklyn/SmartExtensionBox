import serial
import time

ser = serial.Serial('/dev/ttyS0', 9600, timeout=2)
ser.flush()

try:
    while True:
        string = "Test"
        print(string.encode())
        ser.write(string.encode())
        time.sleep(1)
        b = ser.readline()
        string_n = b.decode().rstrip()
        if string_n[0:8] == "Verbruik":
            if string_n[9:] != "":
                print(f"De waarde van string: {string_n[9:]}")
        print(f"De waarde van string: {string_n}")

except KeyboardInterrupt as e:
    print(e)
finally:
    ser.close()
    print("Script has stopped")
