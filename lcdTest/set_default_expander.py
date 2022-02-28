import pygame
import smbus
import time

import os
import RPi.GPIO as GPIO
import sys
sys.path.append("MCP23017-python/src/")

from mcp23017 import *
from i2c import I2C

# Initialize I2C bus for expander board use
i2c = I2C(smbus.SMBus(11))

mcp = MCP23017(0x20, i2c) # MCP23017

#i2c.write_to(0x20, DEFVALA, 0x00)

#bits = i2c.read_from(0x20, DEFVALA)
#print(bits)

mcp.pin_mode(GPA4, OUTPUT)
mcp.pin_mode(GPA3, OUTPUT)

mcp.digital_write(GPA4, HIGH)
mcp.digital_write(GPA3, LOW)

time.sleep(1)
mcp.digital_write(GPA4, LOW)
mcp.digital_write(GPA3, HIGH)

time.sleep(1)
