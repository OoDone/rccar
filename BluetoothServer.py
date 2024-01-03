#!/usr/bin/python

import bluetooth
from Variables import Constants
connected = False
class BluetoothServer:
  def __init__(self, Logger):
    global logger
    global constants
    global buzzer
    logger = Logger
    logger.info("Robot | Code: BluetoothServer.py Initialized.")
    constants = Constants()
    if constants.isTestingMode == False:
      self.StartServer()

  def StartServer(self):
    global connected
    global server_socket
    global client_socket
    server_socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    server_socket.bind((constants.BluetoothConstants().bd_addr, bluetooth.PORT_ANY)) #bluetooth.PORT_ANY
    server_socket.listen(constants.BluetoothConstants().port)
    logger.info("Bluetooth Bind: Listening on port " + str(bluetooth.PORT_ANY))
    bluetooth.advertise_service(server_socket, "Rc Car Server", service_classes=[bluetooth.SERIAL_PORT_CLASS],profiles=[bluetooth.SERIAL_PORT_PROFILE])
    logger.info("Bluetooth: Advertising Service!")
    
    client_socket, address = server_socket.accept()
    logger.info("Bluetooth: Accepting client!")
    logger.info("Bluetooth: Device connected!")

    client_socket.send("connected") #ADD CODE TO HANDLE ON CLIENT SIDE
    connected = True
    
  def return_data(self):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            return data
    except OSError:
        pass
  
  def getServerSocket(self):
    if server_socket != None:
      return server_socket

  def getStatus(self):
    return connected

  def setStatus(self, Connected):
    global connected
    connected = Connected

  def reconnect(self):
    global client_socket
    global address
    client_socket, address = server_socket.accept()
    return client_socket, address

  def getClientSocket(self):
    if client_socket != None:
      return client_socket