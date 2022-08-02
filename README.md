## IMAGE AND MEMO PROGRAM - FTP MICROSERVICE
By Derrick Priebe


#### Summary
- This microservice is designed to provide image file location information to the program upon request.

#### Implementation
- Microservice messaging is handled by ZeroMQ
- Requirements: Python 3.x. Python packages include ZMQ, TIME, and JSON.

#### Client Setup Example
```
# Import packages ZeroMQ, TIME, and JSON
import zmq
import time
import json

# Setup ZMQ and socket to talk to server
context = zmq.Context()
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
```

#### How to Request Data
- An Integer tied to a variable object_id converted to string must be provided in the request

```
## Request Data Example
# Set object ID
object_id = 1
# Convert object ID to string
object_id = str(object_id)
# Send object ID as string message
socket.send_string(object_id)
Actual request data: b“1”
```

#### How to Receive Data
- A string will be returned that can be converted into a dictionary for use

```
## Receive Data Example
# Receive message response as string
message = socket.recv_string()
# Convert string to dictionary format for usage
received_message = json.loads(message)
```

Actual received data: {'object_id': '1', 'file_location': 'ftp://ftp.drivehq.com/image6.jpeg', 'host': 'ftp.drivehq.com', 'file': 'image6.jpeg'}


#### FTP Information
- FTP Site: https://www.drivehq.com
- Username: cs361ftphost
- Password: softwareengineering


#### Requirements
- Python 3.x. Python packages include ZMQ and JSON. TIME is used for Proof of Concept but not likely needed for final implementation.


#### Proof of Concept Testing
- microservice.py and client.py files are available for proof of concept testing
1) Run microservice.py file:
        python3 microservice.py ftp.drivehq.com cs361ftphost softwareengineering
2) Replace image.jpeg with another image.jpeg file in working folder
3) Run client.py file:
        python3 client.py
4) User should see client send an id to the microservice and the microserve send back the id as well as FTP file location


#### Setup
1) Place microservice.py in working folder with “image.jpeg” file that is being replaced.
2) Run the following command to execute the microservice (adding in FTP site, login name, and login password):
python3 microservice.py ftp.drivehq.com cs361ftphost softwareengineering


#### Overall Function
- Every 5 seconds, the microservice checks the file `image.jpeg` in the current folder on the local computer. If the file is updated, then it is uploaded to an FTP server. 
- The images are added to the FTP server with increasing number values attached to them such as `image1.jpeg`, `image2.jpeg`, etc.
- ZeroMQ message server is used to receive an ID value and return the ID value, FTP file location, host and filename. 
- The various information can easily be parsed and utilized for different purposes within the client program.


#### Notes
- Upload information is available upon provision of new file as requested. The microservice does not maintain a database of ID’s, locations, etc outside of the initial upload request as this was out of scope from the original request.
- Modifications to original file uploaded to FTP server are also not in scope for this microservice although new submissions can be uploaded with new image location tagged back to update the original object.
- Assumption is the client manages any relevant ID’s related to program objects.
- Download process is out of scope of the microservice although all the information needed for download is provided to the client. An example download.py file is included to illustrate one instance of a download process.

#### UML Diagram
![](UML_diagram.png)
