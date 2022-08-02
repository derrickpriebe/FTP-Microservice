# Image and Text Program - ZeroMQ Microservice in Python by Derrick Priebe
# Microservice
# Connects REC socket to tcp://localhost:5555

# Import necessary packages
import os
import sys
import time
import ftplib
import hashlib
import pathlib
import zmq
import json

# Load ZeroMQ server on localhost 5555
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# Create references
NAME = "image"
EXTENSION = "jpeg"
FILENAME = NAME + "." + EXTENSION
MD5_FILENAME = "md5"
COUNTER_FILENAME = "counter"
FTP_HOST = sys.argv[1]
FTP_USERNAME = sys.argv[2]
FTP_PASSWORD = sys.argv[3]

def md5():
    return hashlib.md5(pathlib.Path(FILENAME).read_bytes()).hexdigest()

try:
    if len(sys.argv) < 2:
        raise Exception("Pass FTP host as argument")
    with ftplib.FTP(FTP_HOST) as ftp:
        # FTP login
        if len(sys.argv) < 4:
            ftp.login()
        else:
            ftp.login(FTP_USERNAME, FTP_PASSWORD)
            print(f"Connected to {FTP_HOST}")
        if os.path.exists(COUNTER_FILENAME):
            with open(COUNTER_FILENAME, "r") as file:
                counter = int(file.read())
        else:
            counter = 1
        while True:
            try:
                # Error if file not available
                if not os.path.exists(FILENAME):
                    raise Exception(f"File {FILENAME} not found")
                # Read file if available
                if os.path.exists(MD5_FILENAME):
                    with open(MD5_FILENAME, "r") as file:
                        md5_ = file.read()
                else:
                    md5_ = ""
                md5__ = md5()
                if md5_ != md5__:
                    update = True
                else:
                    update = False
                if update:
                    # Check for file change
                    with open(FILENAME, "rb") as file:
                        ftp.storbinary(f"STOR {NAME}{counter}.{EXTENSION}", file)
                    with open(MD5_FILENAME, "w") as file:
                        file.write(md5())
                    # Construct file location parameters
                    file_location = "ftp://"+str(FTP_HOST)+"/"+str(NAME)+str(counter)+"."+str(EXTENSION)
                    file = str(NAME)+str(counter)+"."+str(EXTENSION)
                    # Receive expected ZeroMQ message from client
                    message = socket.recv()
                    message = int(message)
                    print("Received request: %s" % message)
                    # Convert id and file location to JSON
                    message_json = {'object_id':str(message),'file_location':file_location, 'host':FTP_HOST, 'file':file}
                    sendable_message = json.dumps(message_json)
                    print("Sent: %s" % sendable_message)
                    # Send ZeroMQ message reply back to client
                    socket.send_string(sendable_message)
                    # Increase counter for filename and update counter
                    counter += 1
                    with open(COUNTER_FILENAME, "w") as file:
                        file.write(str(counter))
            except Exception as exception:
                print(exception, file=sys.stderr)
            time.sleep(5)
except Exception as exception:
    print(exception, file=sys.stderr)
