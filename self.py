from machine import Pin,PWM
from machine import Timer
import time 
import utime

motor1=Pin(6,Pin.OUT)
motor2=Pin(7,Pin.OUT)
motor3=Pin(8,Pin.OUT)
motor4=Pin(9,Pin.OUT)

enable1=PWM(Pin(0))
enable2=PWM(Pin(1))


trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)


servoPin = Pin(5)
servo = PWM(servoPin)
duty_cycle = 0 

control=0
right=0
left=0
back=0

servo.freq(50)
enable1.freq(1000)
enable2.freq(1000)


enable1.duty_u16(21675)
enable2.duty_u16(21675)

def move_forward():
    motor1.low()
    motor2.high()
    motor3.high()
    motor4.low()
    

def move_backward():
    motor1.high()
    motor2.low()
    motor3.low()
    motor4.high()

def turn_right():
    motor1.low()
    motor2.high()
    motor3.low()
    motor4.high()

def turn_left():
    motor1.high()
    motor2.low()
    motor3.high()
    motor4.low()

def stop():
    motor1.low()
    motor2.low()
    motor3.low()
    motor4.low()
    
def get_distance():
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
       signal = signalon - signaloff
       value = (signal * 0.0343) / 2
   dist = value
   return dist

def setservo(angle):
    duty_cycle = int(angle*(7803-1950)/180) + 1950
    servo.duty_u16(duty_cycle)

setservo(90)

while True:
    distance=get_distance() 
    
    if distance < 15:
        stop()
        move_backward()
        back+=1
        time.sleep(1)
        stop()
        time.sleep(0.5)
        setservo(30) 
        time.sleep(1)
        right_distance=get_distance()
        print(right_distance)
        time.sleep(0.5)
        setservo(150) 
        time.sleep(1)
        left_distance=get_distance()
        print(left_distance)
        time.sleep(0.5)
        setservo(90)
        
        if right_distance > left_distance:
            turn_right()
            right+=1
            time.sleep(0.5)
            stop()
        else:
            turn_left()
            left+=1
            time.sleep(0.5)
            stop()
        
        move_forward()
        time.sleep(1)
        
        if right>0 :
            turn_left()
            right=right-1
            time.sleep(0.5)
            move_forward()
            time.sleep(0.5)
            turn_left()
            time.sleep(0.5)
            move_forward()
            time.sleep(1)
            turn_right()
            time.sleep(0.5)
            stop()
        if left>0 :
            turn_right()
            left=left-1
            time.sleep(0.5)
            move_forward()
            time.sleep(0.5)
            turn_right()
            time.sleep(0.5)
            move_forward()
            time.sleep(1)
            turn_left()
            time.sleep(0.5)
            stop()
        if back>0 :
            move_forward()
            back=back-1
            time.sleep(1)
            stop()
    if control<20 :
        move_forward()
        control+=1

    time.sleep(0.5)
    stop()


