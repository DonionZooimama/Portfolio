import time
import os
import sys
from threading import Thread
sys.path.append(os.path.join(sys.path[0], 'src'))

from InstaAccount import *

file = open('start_info.txt',"r")

#info format [username, password, target audience, follows per hour, unfollows per hour, min following, max following per day]
for line in file:
	info = line.split(',')
	temp = Account(info[0], info[1], info[2], int(info[3]), int(info[4]), int(info[5]), int(info[6])).start()