import serial
from datetime import date
from datetime import datetime

today = date.today()
print (today)

current_time = datetime.now().strftime("%H:%M:%S")
print (current_time)

com = '/dev/cu.usbmodem14101'
ser = serial.Serial(com, '9600')


if ser.is_open == True:
	try:
		while True:
			c = ser.readline().decode() # to convert byte to string
			c = c.rstrip()
			if c.isdigit():
				data = int(c)
				today = date.today()
				current_time = datetime.now().strftime("%H:%M:%S")

				print (f"{data}, {today}, {current_time}")

	except KeyboardInterrupt:
		print ("finished")

	finally:
		ser.close()
		print ("all finished....")


