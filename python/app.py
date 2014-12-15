import zmq
import json
from themes import *
#from Adafruit_PWM_Servo_Driver import PWM
context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect('tcp://localhost:45321')
socket.setsockopt(zmq.SUBSCRIBE, '')

#pwm = PWM(0x40)
#pwm.setPWMFreq(60)

left_handler = Theme()
right_handler = Theme()

def setColor(p, c, (r, g, b)):
  #ri, gi, bi = range(c*4,c*4+3)
  #p.setPWM(ri,0,int(round(r*4095)))
  #p.setPWM(gi,0,int(round(g*4095)))
  #p.setPWM(bi,0,int(round(b*4095)))
  pass

"""
Rainbow(period, intensity)
RandomColors(period, intensity)
Strobe(black_period, light_period)
RandomStrobe(black_period, light_period)
RGBGradient(start, end, period)
HSVGradient(start, end, period)
"""

def theme_to_handler(theme):
	if theme == "calm":
		return Rainbow(6000, 0.2)
	elif theme == "mellow":
		return Rainbow(1200, 0.005)
	elif theme == "study":
		return HSVGradient((.1, 0.31, 1), (.144444444, 0.7, 1), 1000)
	elif theme == "movie1":
		return HSVGradient((0.33,1,0.2),(0.66,1,0.2), 2000)
	elif theme == "movie2":
		return HSVGradient((0.83,1,0.2),(0.95,1,0.2), 2000)
	elif theme == "party":
		return RandomColors(100, 0.8)
	elif theme == "seizure1":
		return Strobe(50,50)
	elif theme == "seizure2":
		return RandomStrobe(60,40)

while True:
	left_color = left_handler.next()
	right_color = right_handler.next()
	setColor(pwm, 0, left_color)
	setColor(pwm, 1, right_color)
	try:
		data_str = socket.recv(flags=zmq.NOBLOCK)
		data = json.loads(data_str);
		if data['type'] == 'color':
			if 'r' in data['strip']:
				right_handler = StaticColor(data['color'])
			if 'l' in data['strip']:
				left_handler = StaticColor(data['color'])
		elif data['type'] == 'theme':
			if 'r' in data['strip']:
				right_handler = theme_to_handler(data['theme'])
			if 'l' in data['strip']:
				left_handler = theme_to_handler(data['theme'])
	except zmq.error.ZMQError:
		continue

