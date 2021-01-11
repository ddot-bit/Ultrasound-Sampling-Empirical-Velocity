import RPi.GPIO as GPIO
from csv import writer
import time
import os.path

GPIO.setmode(GPIO.BCM)
TRIG = 24 # the number is the GPIO PIN number, NOT THE PLUGIN NUMBER OF THE PI
ECHO = 25 # GPIO PIN NUMBER
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
sound_constant = 34300 / 2 # cm/s
print('bootup check')

if not os.path.exists('sornar_data.csv'):
    print('creating new file')
    columns = ['Date', 'Time From Epoch(S)', 'Distance(CM)', 'Deltatime(S)']
    with open('sornar_data.csv', 'a+', newline='') as csvfile:
        csvwriter = writer(csvfile)
        csvwriter.writerow(columns)

def append_file(data, filename='sornar_data.csv'):
    with open(filename, 'a+', newline='') as csvfile:
        csvwriter = writer(csvfile)
        csvwriter.writerow(data)
    return

# finding distance
def compute_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001) #0.01ms to set trigger to low

    GPIO.output(TRIG, False)
    pulse_start = time.time()# are these required?
    pulse_end = time.time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    delta_time = pulse_end - pulse_start # the time it took to read the sound wave

    # use d = v * t, when v is half the speed of sound at sea level @ 343 m/s
    distance = delta_time * sound_constant # cm
    return [round(distance, 3), delta_time]
try:
    while True:
        values = compute_distance()
        distance, delta_time = values[0], values[1]
        local_time = time.asctime()
        append_file([local_time, time.time(), distance, delta_time])
        #print("Time: {0}     Distance: {1}cm.".format(local_time, values[0]))
        time.sleep(1) # allows a second for the user to cancel the loop

except KeyboardInterrupt:
    print("User interuption")
    GPIO.cleanup()
    #close('sonar_sensor.csv')

finally:
    GPIO.cleanup()
    # <file>.close()
    
