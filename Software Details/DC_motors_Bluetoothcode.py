from machine import Pin
import bluetooth
import time

in1 = Pin(22, Pin.OUT)   #leftmotor
in2 = Pin(23, Pin.OUT)

in3 = Pin(19, Pin.OUT)   #rightmotor
in4 = Pin(18, Pin.OUT)

state = ["S"]   

def forward():      #moves forward
    in1.value(1)
    in2.value(0)
    in3.value(1)
    in4.value(0)

def backward():     #moves backward
    in1.value(0)
    in2.value(1)
    in3.value(0)
    in4.value(1)

def left():         #moves left
    in1.value(0)
    in2.value(1)
    in3.value(1)
    in4.value(0)

def right():        #moves right
    in1.value(1)
    in2.value(0)
    in3.value(0)
    in4.value(1)

def stop():
    in1.value(0)
    in2.value(0)
    in3.value(0)
    in4.value(0)



name = "RoboSumo-P1"
ble = bluetooth.BLE()
ble.active(False)
time.sleep(0.5)
ble.active(True)
ble.config(gap_name=name)

service_UUID = bluetooth.UUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e")
char_UUID    = bluetooth.UUID("6e400002-b5a3-f393-e0a9-e50e24dcca9e")

char    = (char_UUID, bluetooth.FLAG_WRITE)
service = (service_UUID, (char,),)
((char_handle,),) = ble.gatts_register_services((service,))

def event_occured(event, data):
    if event == 1:
        print("Connected")
    elif event == 2:
        print("Disconnected")
        advertise(name)
    elif event == 3:
        conn_handle, value_handle = data
        if value_handle == char_handle:
            raw = ble.gatts_read(char_handle).rstrip(b'\x00')
            state[0] = raw.decode().strip()
            print("CMD:", state[0])

def advertise(device_name):
    nb = device_name.encode()
    adv = bytearray([0x02, 0x01, 0x06]) + bytearray([len(nb)+1, 0x09]) + nb
    ble.gap_advertise(50, adv_data=adv)
    print("Advertising:", device_name)

advertise(name)
ble.irq(event_occured)

while True:
    if state[0] == "F":
        forward()
     print("moved forward")
    elif state[0] == "B":
        backward()
        print("moved backward")
    elif state[0] == "L":
        left()
        print("moved left")
    elif state[0] == "R":
        right()
        print("moved left")
    elif state[0] == "S":
        stop()
        print("stopped")
    time.sleep(0.05)
