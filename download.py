# Image and Text Program - ZeroMQ Microservice in Python by Derrick Priebe
# Download Proof of Concept

# Import Module
import ftplib
from PIL import Image
from io import BytesIO
 
# Fill Required Information
HOSTNAME = "ftp.drivehq.com"
USERNAME = "cs361ftphost"
PASSWORD = "softwareengineering"
 
# Connect FTP Server
ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

# Enter File Name with Extension
filename = "image3.jpeg"
 
# Write file in binary mode
with open(filename, "wb") as file:
    # Command for Downloading the file "RETR filename"
    ftp_server.retrbinary(f"RETR {filename}", file.write)
 
# Get list of files
ftp_server.dir()

# Close the Connection
ftp_server.quit()