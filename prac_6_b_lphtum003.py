import socket
import threading
from time import sleep, clock, time
from gpiozero import MCP3008

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 10000))

sock.listen(1)

connections = []

ldr = MCP3008(5)

def set_config(config):
	t1=time()
	while True:
		t2 = time()
		positive_count=1
		negative_count=1
		count = 0
		while config=="W":
			while t2 - t1 < 1:
				current_light = ldr.value*100
				sleep(0.1)
				next_light = ldr.value*100
				if next_light//1 > current_light//1:
					count+=1
				t2 = time()
			speed_of_wave = count
			temp = t2
			t1 = temp
			print("%-3dwaves per second" % (speed_of_wave))
			count=0
		while config=="+":
			positive_count+=1
			negative_count=1
                        while t2 - t1 < 1:
                                current_light = ldr.value*100
                                sleep(0.1)
                                next_light = ldr.value*100
                                if next_light//1 > current_light//1+1*positive_count:
                                        count+=1
                                t2 = time()
                        speed_of_wave = count
                        temp = t2
                        t1 = temp
                        print("%-3dwaves per second" % (speed_of_wave))
                        count=0

		while config=="-":
			negative_count+=1
			positive_count=1
                        while t2 - t1 < 1:
                                current_light = ldr.value*100
                                sleep(0.1)
                                next_light = ldr.value*100
                                if next_light//1 > current_light//1-1*negative_count:
                                        count+=1
                                t2 = time()
                        speed_of_wave = count
                        temp = t2
                        t1 = temp
                        print("%-3dwaves per second" % (speed_of_wave))
                        count=0


def handler(c, a):
        global connections
	global config
        help="Select one of the following commands:\n{\n\tW:ON,\n\tO:OFF,\n\t+:+100,\n\t-:-100\n}\n"

        while True:
                for connection in connections:
                        connection.send(help)

		data = c.recv(1024)

		if data[0]=="W":
			config="W"
                	for connection in connections:
                        	connection.send("ON\n")
		elif data[0]=="O":
			for connection in connections:
				connection.send("OFF\n")
				c.close()
				break
		elif data[0]=="+":
                        config="+"
			for connection in connections:
				connection.send("+1\n")
		elif data[0]=="-":
                        config="-"
			for connection in connections:
				connection.send("-1\n")
		if not data:
                        connections.remove(c)
                        c.close()
			break
		wave_thread = threading.Thread(target=set_config, args=(config))
	        wave_thread.start()


while True:
	c, a = sock.accept()
	connection_thread = threading.Thread(target=handler, args=(c, a))
	connection_thread.daemon = True
	connection_thread.start()
	connections.append(c)
	print(c)
