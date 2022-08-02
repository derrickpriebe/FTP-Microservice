# Image and Text Program - ZeroMQ Client Proof of Concept by Derrick Priebe
# Client Proof of Concept
# Connects REQ socket to tcp://localhost:5555

# Note: This program is for client Proof of Concept purpose only. It is expected that the program communicating with the microservice may be implemented somewhat differently based on program specifics and preferences.

# Import packages ZeroMQ, TIME, and JSON
import zmq
import time
import json

# Setup ZMQ and socket to talk to server on localhost 5555
context = zmq.Context()
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Set object ID
object_id = 1

for request in range(1):
    # Send request
    print("Sending request %s …" % request)
    object_id = str(object_id)
    socket.send_string(object_id)
    print("Sent object [ %s ] …" % object_id)
    time.sleep(5)

    # Get the reply
    message = socket.recv_string()
    received_message = json.loads(message)
    print("Received reply %s [ %s ]" % (request, received_message))