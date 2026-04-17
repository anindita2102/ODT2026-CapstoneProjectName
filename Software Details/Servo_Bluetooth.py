
from machine import Pin, PWM
import bluetooth
import time

servo1 = PWM(Pin(16), freq=50)
servo2 = PWM(Pin(17), freq=50)

state = ["N"]   # "A" = attack, "N" = neutral

def arms_neutral():
    servo1.duty(35)
    time.sleep(0.1)
    servo2.duty(35)
    time.sleep(0.1)

def arms_attack():
    servo1.duty(115)
    time.sleep(0.1)
    servo2.duty(115)
    time.sleep(0.1)

name = "RoboSumo-P1"
ble  = bluetooth.BLE()
ble.active(False); time.sleep(0.5); ble.active(True)
ble.config(gap_name=name)

service_UUID = bluetooth.UUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e")
char_UUID    = bluetooth.UUID("6e400002-b5a3-f393-e0a9-e50e24dcca9e")

char    = (char_UUID, bluetooth.FLAG_WRITE)
service = (service_UUID, (char,),)
((char_handle,),) = ble.gatts_register_services((service,))

def event_occured(event, data):
    if event == 2:
        advertise(name)
    elif event == 3:
        conn_handle, value_handle = data
        if value_handle == char_handle:
            raw = ble.gatts_read(char_handle).rstrip(b'\x00')
            state[0] = raw.decode().strip()

def advertise(device_name):
    nb  = device_name.encode()
    adv = bytearray([0x02,0x01,0x06]) + bytearray([len(nb)+1,0x09]) + nb
    ble.gap_advertise(50, adv_data=adv)

advertise(name)
ble.irq(event_occured)
arms_neutral()

while True:
    if state[0] == "A":
        arms_attack()
        time.sleep(0.5)    # hold attack position 
        arms_neutral()
        state[0] = "N"
    time.sleep(0.05)
