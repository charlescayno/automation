"""IMPORT DEPENDENCIES"""
from time import time, sleep
import sys
from powi.equipment import tts, prompt
##################################################################################\

message = sys.argv[1]
tts(message)

sleep(2)