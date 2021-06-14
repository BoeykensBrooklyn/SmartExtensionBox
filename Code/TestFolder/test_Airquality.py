from AirQualitySensor import AirQualitySensor
import time

airsensor = AirQualitySensor()

try:
    while True:
        air_quality_now = airsensor.read_channel()
        print(f"\n------------Information------------")
        print(f"Air quality is: {air_quality_now}")

        time.sleep(1)
except KeyboardInterrupt as e:
    print(e)
finally:
    print("Script has stopped")
