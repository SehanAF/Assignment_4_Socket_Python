import socket
import logging

logging.basicConfig(
 level=logging.INFO,
 format="%(asctime)s [%(levelname)s] %(message)s",
 handlers=[
  logging.FileHandler("server.log"),
  logging.StreamHandler()
 ]
)

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.100.3"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
 client.connect(ADDR)
 logging.info(f"Connected to server at {ADDR}")
except socket.error as e:
 logging.error(f"Failed to connect to server: {e}")


def send(msg):
 try:
  message = msg.encode(FORMAT)
  msg_length = len(message)
  send_length = str(msg_length).encode(FORMAT)
  send_length += b' ' * (HEADER - len(send_length))
  client.send(send_length)
  client.send(message)
  logging.info(f"Sent message: {msg}")
  response = client.recv(2048).decode(FORMAT)
  logging.info(f"Received response: {response}")
 except socket.error as e:
  logging.error(f"Failed to send message: {e}")

send("Hello World!")
send("Hello Everyone!")
send("Hello There!")

try:
 send(DISCONNECT_MESSAGE)
finally:
 client.close()
 logging.info("Connection closed")