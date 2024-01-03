class Constants:
    isTestingMode = False

    class DriveConstants:
        motorPin = 4
        motorNeutralSpeed = 1500
        motorMinSpeed = 1000
        motorMaxSpeed = 2000

        #Steering Servos
        servoPin = 18
        servoNeutralPosition = 1488 #1488 for 556-2420 & 1700 for 1500-1900
        directionTicksPer = 9 #2
        servoMaxLimitTicks = 2388 #1900
        servoMinLimitTicks = 588 #1500

    class BluetoothConstants:
        bd_addr = "" #Leave blank to accept connections from any device, enter a address to only allow a specific device
        #Example bd_addr = "DC:A6:32:6B:38:BD"  
        #"B8:27:EB:D6:57:CE" 
        #B8:27:EB:6B:AB:4B
        #uuid = "42b58f76-b26d-11ea-b733-cb205305bc99"
        port = 1

