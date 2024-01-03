#!/usr/bin/python

import os
from time import sleep
from Variables import Constants
try:
    import pigpio
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()
    import RPi.GPIO as GPIO

position = 0.0
servo = False

class Servo:
  def __init__(self, servoPin, Logger):
    global servo
    global logger
    global constants
    global pi
    logger = Logger
    logger.info("Robot | Code: Servo.py Init.")
    constants = Constants()
    servo = servoPin
    GPIO.setmode(GPIO.BCM)
    if constants.isTestingMode == False:
      os.system("sudo pigpiod")
      sleep(1)
      pi = pigpio.pi()
      pi.set_servo_pulsewidth(servo, 0)
    
  def setServoPosition(self,Position):
    if not Position > constants.DriveConstants().servoMaxLimitTicks and not Position < constants.DriveConstants().servoMinLimitTicks:
      if constants.isTestingMode == False:
        pi.set_servo_pulsewidth(servo, Position)
      else: logger.info("TestMode: Set Servo Position to " + str(Position))
    else: logger.info("setServoPosition: Position not within allowed position range.")

  def setServoPositionPercent(self,positionPercent):
    if positionPercent > -101 and positionPercent < 101:
      position = 0.0
      if positionPercent > 0:
        position = constants.DriveConstants().servoNeutralPosition - positionPercent * constants.DriveConstants().directionTicksPer
      else:
        position = -positionPercent * constants.DriveConstants().directionTicksPer + constants.DriveConstants().servoNeutralPosition
      if constants.isTestingMode == False:
        pi.set_servo_pulsewidth(servo, position)
      else: logger.info("TestMode: Set Servo Position to " + str(position) + "(" + str(positionPercent) + "%)")
    else: logger.info("setServoPositionPercent: positionPercent not within allowed position range.")
    
  def stopServo(self):
    if constants.isTestingMode == False:
      pi.set_servo_pulsewidth(servo, 0.0)
    else: logger.info("TestMode: Stopping Servo...")
    
  def getServoPosition(self):
    return position