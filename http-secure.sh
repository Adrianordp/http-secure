#!/bin/bash
while true
do
	echo "Openning http server"
	# Creates a password protected http server
	# ...on folder /home/
	# ...opened to all interfaces
	# ...protected by a password file
	python3 /home/adriano/git/http-secure/http-secure.py -d /home/ -b 0.0.0.0 -f /home/adriano/.passwd-files/http-secure.passwd

	# Sleep for 5 seconds before trying to reopen the socket
	sleep 5
done
