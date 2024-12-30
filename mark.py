from flask import session
import serial
import mysql.connector
from mysql.connector import Error
from modules import *
from datetime import datetime

# Set up the serial connection (update COM port to match your system)
arduino_port = "COM5"  # Update this to your Arduino's port
baud_rate = 9600  # Must match the baud rate in the Arduino code
