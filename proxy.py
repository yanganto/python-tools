"""
A tool for proxy

USAGE:
	proxy.py [-v] [-h] [local_host:port] [remote_host:port] [receive_first]

	-v, --verbose
		verbose mode

	-h, --help
		print usage

	-h, --hexdump
		dump buffer as hex

EXAMPLE:
	proxy.py 127.0.0.1:80 10.12.132.1:8080

"""

import sys
import socket
import threading
import getopt

verbose = False
timeout = 5
hexdump = False


def proxy_handler(client_socket, remote_host, remote_port, receive_first):

	remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	remote_socket.connect((remote_host, remote_port))

	if receive_first:
		remote_buffer = receive_from(remote_socket)
		if verbose:
			print(remote_buffer)

		remote_buffer = response_handler(remote_buffer)

		if remote_buffer:
			if verbose:
				print('[<==] received from remote host.')
			client_socket.send(remote_buffer)
			if verbose:
				print("[<==] sent to local host.")

	while True:
		local_buffer = receive_from(client_socket)

		if local_buffer:
			if verbose:
				print('[==>] received from local host.')
				print(local_buffer)
			local_buffer = request_handler(local_buffer)
			remote_socket.send(local_buffer)
			if verbose:
				print("[<==] sent to remote host.")

		remote_buffer = receive_from(remote_socket)

		if remote_buffer:
			if verbose:
				print('[<==] received from remote host.')
				print(remote_buffer)
			remote_buffer = response_handler(remote_buffer)
			client_socket.send(remote_buffer)
			if verbose:
				print("[<==] sent to local host.")

		if not remote_buffer and not local_buffer:
			remote_socket.close()
			client_socket.close()
			if verbose:
				print('Closing..')
				break


def request_handler(request_buffer):
	return request_buffer

def response_handler(response_buffer):
	return response_buffer

def receive_from(socket):

	buffer = b''
	socket.settimeout(timeout)
	try:
		while True:
			data = socket.recv(4096)
			if not data:
				break
			buffer += data
	except:
		pass

	return buffer


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		server.bind((local_host, local_port))

	except:
		print("Failed to listen on {}:{}".format(local_host, local_port))
		sys.exit(0)

	if verbose:
		print('Listen on {}:{}'.format(local_host, local_port))
	server.listen(5)

	while True:
		client_socket, addr = server.accept()
		if verbose:
			print("[==>] Received from {}:{}".format(addr[0], addr[1]))
		proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port,
																	receive_first))
		proxy_thread.start()


def main():
	global verbose
	options = list(filter(lambda x: x[0] == '-', sys.argv[1:]))
	opts, args = getopt.getopt(options, "vh", ['verbose', 'help'])
	for o, a in opts:
		if o in ('-h', '--help'):
			print(__doc__)
			sys.exit(0)
		elif o in ('-v', '--verbose'):
			verbose = True

	args = list(filter(lambda x: x[0] != '-', sys.argv[1:]))

	if len(args) < 2:
		print("Missing arguments.")
		print(__doc__)
		sys.exit(1)
	local_host = args[0].split(':')[0]
	local_port = int(args[0].split(':')[1])
	remote_host = args[1].split(':')[0]
	remote_port = int(args[1].split(':')[1])

	receive_first = False if len(args) < 2 else True

	if verbose:
		print('local: {}:{}'.format(local_host, local_port))
		print('remote: {}:{}'.format(remote_host, remote_port))
		if receive_first:
			print("Receive First")


	server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == '__main__':
	main()

