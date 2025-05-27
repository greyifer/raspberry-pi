import RPi.GPIO as GPIO  # type: ignore
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 20
ECHO = 21
TRIG1 = 16
ECHO1 = 12
TRIG2 = 26
ECHO2 = 19
TRIG3 = 13
ECHO3 = 6
TRIG4 = 24
ECHO4 = 23

print("Distance measuring...")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(TRIG3, GPIO.OUT)
GPIO.setup(ECHO3, GPIO.IN)
GPIO.setup(TRIG4, GPIO.OUT)
GPIO.setup(ECHO4, GPIO.IN)

GPIO.output(TRIG, False)
GPIO.output(TRIG1, False)
GPIO.output(TRIG2, False)
GPIO.output(TRIG3, False)
GPIO.output(TRIG4, False)

# Sensor 1
print("Waiting for sensor 1 to send signal")
time.sleep(2)
GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)
print("Reading sensor 1")
while GPIO.input(ECHO) == 0:
    pulse_start = time.time()
while GPIO.input(ECHO) == 1:
    pulse_end = time.time()
pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17150
distance = round(distance, 2)
distance_sensor1 = distance
print("Distance sensor 1:", distance, "cm")

# Sensor 2
print("Waiting for sensor 2 to send signal")
time.sleep(2)
GPIO.output(TRIG1, True)
time.sleep(0.00001)
GPIO.output(TRIG1, False)
print("Reading sensor 2")
while GPIO.input(ECHO1) == 0:
    pulse_start = time.time()
while GPIO.input(ECHO1) == 1:
    pulse_end = time.time()
pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17150
distance = round(distance, 2)
distance_sensor2 = distance
print("Distance sensor 2:", distance, "cm")

# Sensor 3
print("Waiting for sensor 3 to send signal")
time.sleep(2)
GPIO.output(TRIG2, True)
time.sleep(0.00001)
GPIO.output(TRIG2, False)
print("Reading sensor 3")
while GPIO.input(ECHO2) == 0:
    pulse_start = time.time()
while GPIO.input(ECHO2) == 1:
    pulse_end = time.time()
pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17150
distance = round(distance, 2)
distance_sensor3 = distance
print("Distance sensor 3:", distance, "cm")

# Sensor 4
print("Waiting for sensor 4 to send signal")
time.sleep(2)
GPIO.output(TRIG3, True)
time.sleep(0.00001)
GPIO.output(TRIG3, False)
print("Reading sensor 4")
while GPIO.input(ECHO3) == 0:
    pulse_start = time.time()
while GPIO.input(ECHO3) == 1:
    pulse_end = time.time()
pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17150
distance = round(distance, 2)
distance_sensor4 = distance
print("Distance sensor 4:", distance, "cm")

# Sensor 5
print("Waiting for sensor 5 to send signal")
time.sleep(2)
GPIO.output(TRIG4, True)
time.sleep(0.00001)
GPIO.output(TRIG4, False)
print("Reading sensor 5")
while GPIO.input(ECHO4) == 0:
    pulse_start = time.time()
while GPIO.input(ECHO4) == 1:
    pulse_end = time.time()
pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17150
distance = round(distance, 2)
distance_sensor5 = distance
print("Distance sensor 5:", distance, "cm")

GPIO.cleanup()