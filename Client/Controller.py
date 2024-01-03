#!/usr/bin/python

import pygame
import bluetooth
from Logger import Logger
import sys
from timer import Timer
from time import sleep

#0 = X
#1 = CIRCLE
#2 = TRIANGLE
#3 = SQUARE
#4 = L1
#5 = R1
#6 = L2
#7 = R2
#8 = SHARE
#9 = OPTIONS
#10 = PS4 BUTTON
#11 = LEFT ANALOG PRESS 
#12 = RIGHT ANALOG PRESS



bluetoothAddress = "64:49:7d:91:27:46" #Mine "DC:A6:32:6B:38:BD"      #School other"B8:27:EB:D6:57:CE"  
#School server: B8:27:EB:6B:AB:4B
stickDeadband = 3
logger = Logger("clientLog")
joy = False
speed = False
direction = False
connected = False
ready = False
enabled = False

def return_data():
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            return data
    except OSError:
        pass



def init():
    global sock
    global j
    global connected
    global joy
    global ready
    ready = False
    connected = False
    joy = False
    timer = Timer()
    timer.start()
    while not connected:
        if timer.hasElapsed(3):
            timer.reset()
            try:
                if not connected:
                    pygame.display.init()
                    pygame.joystick.init()
                    j = pygame.joystick.Joystick(0)
                    j.init()
                    joy = True
            except:
                pygame.quit()
                joy = False
                logger.warning("No Joystick Detected")
            try:
                if not connected and joy:
                    sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
                    sock.connect((bluetoothAddress, 1))
                    sock.setblocking(False)
                    joy = False
                    connected = True
                    timer.stop()
                    logger.info("Client: Connected To Robot!")
            except:
                logger.warning("Bluetooth: Cannot find Bluetooth Server")

def enableRobot():
    global enabled
    if connected:
        if not enabled:
            if ready:
                sock.send("en")
                logger.info("Client: Sending Enable Request!")
            else:
                logger.info("Client: Robot Still Starting.")
        else:
            logger.info("Client: Robot already Enabled.")
    else:
        logger.info("Client: Not Connected To Robot")

def disableRobot():
    if connected:
        sock.send("di")
        logger.info("Client: Sending Disable Request!")
    else:
        logger.info("Client: Not Connected To Robot")    
def stopRobot():
    if connected:
        sock.send("s")
    else:
        logger.info("Client: Not Connected To Robot")

def squareDown():
    if connected:
        sock.send("xd")
    else:
        logger.info("Client: Not Connected To Robot")

def squareUp():
    if connected:
        sock.send("xd")
    else:
        logger.info("Client: Not Connected To Robot")

init()

def loop():
    global loopTimer
    if loopTimer.hasElapsed(0.02):
        loopTimer.reset()
        if enabled:
            global speed
            global direction
            try:
                speed = float(round(j.get_axis(1) * -100))
                direction = float(round(j.get_axis(3) * 100)) #axis 0
                if direction < stickDeadband and direction > -stickDeadband:
                    direction = 0.0
                if speed >= -100 and direction >= -100:
                    sock.send(":M:" + str(speed) + ":D:" + str(direction))
            except:
                logger.warn("EXCEPTION: LOOP FUNCTION INFO: sysinfo: " + str(sys.exc_info()[0]) + " speed: " + str(speed) + " direction: " + str(direction))
        
x = False
circle = False
square = False
triangle = False 
global loopTimer
loopTimer = Timer()
loopTimer.start() 
while connected:
    try: 
        sock.getpeername()
        connected = True
    except:
        connected = False
        enabled = False
        init()
    try:
        loop()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if j.get_button(0) and not x: #X
                    disableRobot()
                    x = True
                if j.get_button(1) and not circle: #circle
                     enableRobot()
                     circle = True
                if j.get_button(2) and not triangle: #Triangle
                    #DOES NOTHING
                    triangle = True
                if j.get_button(3) and not square: #Square
                    #DOES NOTHING
                    square = True
            elif event.type == pygame.JOYBUTTONUP:
                if x and not j.get_button(0): #X
                    x = False
                elif circle and not j.get_button(1): #circle
                    circle = False
                elif triangle and not j.get_button(2): #triangle
                    triangle = False
                elif square and not j.get_button(3): #square
                    square = False
                
        data=return_data()
        if data is not None:
            if bytes(':','UTF-8') in data:
                xd = data.decode('UTF-8').split(":")[1]
                print("Collision warning " + xd + " cm")
            elif bytes('enable','UTF-8') in data:
                logger.info("Robot | Enabled Robot.")
                enabled = True
            elif bytes('disable','UTF-8') in data:
                enabled = False
                logger.info("Robot | Disabled Robot.")
            elif bytes('ready','UTF-8') in data:
                ready = True
                logger.info("Robot | Robot Started.")
            else:
                try:
                    data = return_data().replace("b'", "").replace("'","")
                    logger.info("Robot | " + data)
                except:
                    logger.warn("Cannot use .replace Line 103")
              
  
               
    except KeyboardInterrupt:
        disableRobot()
        print("EXITING NOW")
        j.quit()
        data.toString()