#!/usr/bin/python

from Logger import Logger
#try:
from BluetoothServer import BluetoothServer
#except:
    #print("Cannot Import BluetoothServer")
from Variables import Constants

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()
    import RPi.GPIO as GPIO

from drive.Motor import Motor
from drive.Servo import Servo


try:
    logger = Logger("/home/pi/Desktop/logs/rcCarLog")
except:
    logger = Logger("rcCarLog")


constants = Constants()
try:
    if not constants.isTestingMode:
        blServer = BluetoothServer(logger)
except:
    logger.info("Exception occurred while Initializing BluetoothServer.py")
enabled = False
disconnected = False
client_socket = None

driveMotor = Motor(1, logger) #FIX MOTOR PIN
steerServo = Servo(1, logger) #FIX SERVO PIN

GPIO.setmode(GPIO.BCM)         #Set GPIO pin numbering
logger.info("Car | Code: Main.py Init")


def enableCar():
    global enabled
    if not enabled:
        enabled = True
        logger.info("Car | Enabled Car.")
        if constants.isTestingMode == True:
            logger.info("Car | Car in Test Mode!")
        if constants.isTestingMode == False and blServer.getStatus() == True:
            client_socket.send("enable")
    else:
        logger.info("Car | Car Already Enabled.")

def disableCar():
    global enabled
    if enabled:
        enabled = False
        driveMotor.stopMotor()
        logger.info("Car | Disabled Car.")
        try:
            if constants.isTestingMode == False and blServer.getStatus() == True:
                client_socket.send("disable")
        except:
            logger.warning("Car | Couldnt Inform Client Of New Status: Disabled")
    else:
        logger.info("Car | Car Already Disabled")

def driveCar(y):
    speed = y.decode('UTF-8').split(':')[2].replace("'",'')
    direction = y.decode('UTF-8').split(':')[4].replace("'",'')
    #TESTMODE FAKE BYTE:   0:1:10:3:0
    try:
      speed = float(speed)
      direction = float(direction)
    except:
      speed = 0.0
      direction = 0.0
      logger.warn("Exception: speed or direction not a number")

      driveMotor.setMotorSpeedPercent(speed)
      steerServo.setServoPositionPercent(direction)

while(1):
    try:
        #if not constants.isTestingMode: #True is not on(Car disabled)
            #if enabled:
                #disableCar() #Disable car every time its enabled while the kill switch is active(In off position)
        if constants.isTestingMode == True:
            if enabled == False:
                enableCar()
            x=bytes(input(), 'utf-8')
        else:
            x=blServer.return_data()
            if blServer.getStatus():
                if client_socket is None:
                    client_socket = blServer.getClientSocket()
                    client_socket.send("ready")
                    logger.info("READY")
        if x == None:
            if constants.isTestingMode == False:
                logger.info("Bluetooth: disconnected!")
                driveMotor.stopMotor()
                disconnected = True
                blServer.setStatus(False)
                client_socket, address = blServer.reconnect()
                if disconnected == True:
                    client_socket.send("ready")
                    blServer.setStatus(True)
                    logger.info("Bluetooth: Reconnected!")
        elif bytes(':','UTF-8') in x:
            if enabled == True:
                driveCar(x)
        elif x==bytes('s', 'UTF-8'):
            driveMotor.stopMotor()
            logger.info("Stopping car...")
            x='z'
        elif x==bytes('en', 'UTF-8'):
            logger.info("Enabling Car...")
            enableCar()
            x='z'
        elif x==bytes('di', 'UTF-8'):
            logger.info("Disabling Car...")
            disableCar()
            x='z'
        elif x==bytes('e', 'UTF-8'):
            GPIO.cleanup()
            break
        else:
            client_socket.send("<<<  wrong data  >>>")
            client_socket.send("please enter the defined data to continue.....")
    except:
        logger.info("Car | Error in Main Loop, Shutting down program(Change to continue and not crash?).")
        disableCar()
        GPIO.cleanup()
        crash.toString()