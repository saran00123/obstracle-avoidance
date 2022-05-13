from machine import Pin,PWM 
import time
import utime

led  = Pin(25,Pin.OUT)

motor1=Pin(10,Pin.OUT)
motor2=Pin(11,Pin.OUT)
motor3=Pin(6,Pin.OUT)
motor4=Pin(7,Pin.OUT)
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
i=0
servo.freq(50)
enable1.freq(1000)
enable2.freq(1000)

enable1.duty_u16(45025)
enable2.duty_u16(45025)

def move_forward():
    enable1.duty_u16(25025)
    enable2.duty_u16(25025)
    motor1.low()
    motor2.high()
    motor3.high()
    motor4.low()
    
def move_backward():
    enable1.duty_u16(25025)
    enable2.duty_u16(25025)
    motor1.high()
    motor2.low()
    motor3.low()
    motor4.high()
    
def turn_right():
    enable1.duty_u16(45025)
    enable2.duty_u16(45025)
    motor1.low()
    motor2.high()
    motor3.low()
    motor4.high()
    
def turn_left():
    enable1.duty_u16(45025)
    enable2.duty_u16(45025)
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
   timepassed = signalon - signaloff
   dist = (timepassed * 0.0343) / 2
   return dist

def setservo(angle):
    duty_cycle = int(angle*(7803-1950)/180) + 1950
    servo.duty_u16(duty_cycle)

setservo(90)

while True:
    led.value(1)
    distance=get_distance() 
    if i<30 :
        move_forward()
        time.sleep(0.1)
        print(i)
    else:
        stop()
    if distance < 20:
        stop()
        move_backward()
        back+=1
        time.sleep(0.5)
        stop()
        time.sleep(0.5)
        setservo(30) 
        time.sleep(1)
        right_distance=get_distance()
        time.sleep(0.5)
        setservo(150) 
        time.sleep(1)
        left_distance=get_distance()
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
            right=right-1
            turn_left()
            time.sleep(0.5)
            move_forward()
            time.sleep(1)
            turn_left()
            time.sleep(0.5)
            move_forward()
            time.sleep(1)
            turn_right()
            time.sleep(0.5)
            stop()
        if left>0 :
            left=left-1
            turn_right()
            time.sleep(0.5)
            move_forward()
            time.sleep(1)
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
            time.sleep(0.5)
            stop()
    time.sleep(0.1)
    i+=1;
stop()



