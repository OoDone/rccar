#!/usr/bin/python

import os
from time import sleep
from Variables import Constants
#from Encoder import Encoder
try:
    import pigpio
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()
    import RPi.GPIO as GPIO

speed = 0.0
motor = False
ticks = 5

class Motor:
  def __init__(self, motorPin, Logger):
    global motor
    global logger
    global constants
    global pi
    global e1
    motor = motorPin
    logger = Logger
    logger.info("Robot | Code: Motor.py Init.")
    constants = Constants()
    GPIO.setmode(GPIO.BCM)
    #e1 = Encoder(21, 20)
    #e1 = Encoder(20, 21)
    #A GPIO 20, B GPIO 21
    if constants.isTestingMode == False:
      os.system("sudo pigpiod")
      sleep(1)
      pi = pigpio.pi()
      pi.set_servo_pulsewidth(motor, 0)
    

  def setMotorSpeed(self,Speed):
    if (Speed <= constants.DriveConstants().motorMaxSpeed and Speed >= constants.DriveConstants().motorMinSpeed) or Speed == 0:
      if constants.isTestingMode == False:
        speed = Speed
        pi.set_servo_pulsewidth(motor, speed)
      else:
        logger.info("TestMode: Set Motor Speed to " + str(Speed))
    else:
      logger.info("setMotorSpeed: Speed not within allowed speed range.")

  def setMotorSpeedPercent(self,speedPercent):
    if speedPercent >= -100 and speedPercent <= 100:
      speed = 0.0
      if speedPercent > 0:
        speed = constants.DriveConstants().motorNeutralSpeed+speedPercent*5
      else:
        speed = speedPercent*5+constants.DriveConstants().motorNeutralSpeed
      if constants.isTestingMode == False:
        pi.set_servo_pulsewidth(motor, speed)
      #else: logger.info("TestMode: Set Motor Speed to " + str(speedPercent) + " Percent.")
    else: logger.info("setMotorSpeedPercent: SpeedPercent not within allowed speed range.")
    
  def stopMotor(self):
    if constants.isTestingMode == False:
      pi.set_servo_pulsewidth(motor, 0.0)
    else: logger.info("TestMode: Stopping motor...")
    
  def getMotorSpeed(self):
    return speed

  def getFakeEncoderTicks(self):
    return ticks

  #def getEncoderTicks(self):
    #return e1.read()

  def setEncoderTicks(self, Ticks):
    global ticks
    ticks = Ticks