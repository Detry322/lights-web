import zmq
import json
context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect('tcp://localhost:45321')
socket.setsockopt(zmq.SUBSCRIBE, '')

handler = None

while True:
	#get next color in handler
	#send the color of the PWM
	try:
		data_str = socket.recv(flags=zmq.NOBLOCK)
		data = json.loads(data_str);
		if data['type'] == 'color':
			#set the handler to be a color_enumerator of said color
			print data['color']
			pass
		elif data['type'] == 'theme':
			#set the handler to bea color enumerator of different color
			pass
	except zmq.error.ZMQError:
		continue

