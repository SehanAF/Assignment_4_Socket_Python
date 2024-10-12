# Import Libary
import logging
import socket
import threading

# setup logging
logging.basicConfig(
 level=logging.INFO,
 format="%(asctime)s [%(levelname)s] %(message)s",
 handlers=[
  logging.FileHandler("server.log"),
  logging.StreamHandler()
 ]
)

# Konfigurasi Server
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
HEADER = 64

# Inisialisasi Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Function handle_client
def handle_client(conn, addr):
 logging.info(f"[NEW CONNECTION] {addr} connected.")
 connected = True
 try:
  while connected:
   msg_length = conn.recv(HEADER).decode(FORMAT)
   if msg_length:
    msg_length = int(msg_length)
    msg = conn.recv(msg_length).decode(FORMAT)
    if msg == DISCONNECT_MESSAGE:
     connected = False
    print(f"[{addr}] {msg}")
    conn.send("Message received".encode(FORMAT))
 except ConnectionResetError:
  logging.warning(f"[ERROR] Connection with {addr} was reset.")
 finally:
  conn.close()
  logging.info(f"[DISCONNECTED] {addr} disconnected.")

# Function start
def start():
 server.listen()
 logging.info(f"[LISTENING] Server is listening on {SERVER}")
 while True:
  conn, addr = server.accept()
  thread = threading.Thread(target=handle_client, args=(conn, addr))
  thread.start()
  logging.info(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

# running server
if __name__ == "__main__":
 print("[STARTING] server is starting.... ")
 start()
 



