import socket as sock
import re

DB = {"admin123":"pass123" }
cusswords = ["idiot","fool"]
def check_cusswords(msg):
    for word in cusswords:
        if word in msg.lower():
            return True
    return False

def contains_contact_info(msg):
    email_p = r"[a-zA-Z0-9-#%_.]+@[a-zA-Z0-9#%.-]+\.[a-zA-Z0-9.]+$"
    phone_p = r"(\+91-)?[0-9]\d{9}$"
    return re.search(phone_p, msg) or re.search(email_p, msg)

def start_server():
    host = "0.0.0.0"
    port = 1234

    server_sock = sock.socket(sock.AF_INET,sock.SOCK_STREAM)            # Creating a socket for server
    server_sock.bind((host,port))                                       # Binding the server at port number 1234 and accepting from all host i.e 0.0.0.0
    server_sock.listen(1)                                               # Server is now listening
    print(f"Server is listening at PORT: {port}")                          

    conn , addr = server_sock.accept()                                  # If any connection is made conn -> socket of connected client
    print(f"Connected to {addr}")                                       # addr -> address of the connected client


    # Authenticate for valid user
    conn.send(b"Username: ")
    user_id = conn.recv(512).decode()
    
    conn.send(b"Password: ")
    password = conn.recv(512).decode()
        
    if DB.get(user_id) != password:
        print("Authentication Failed!!...")
        conn.send(b"Authentication Failed!!")
    else:
        print("Authentication Done!!!!")
        conn.send( b"Authenticated ...You can Chat (USE bye to disconnect)\n")

        while True:
            # Receiving msg from client
            msg = conn.recv(512).decode() 
            if not msg or msg.lower() == "bye": 
                print("Client disconnected.")
                break
                
            # Check for cussword
            if check_cusswords(msg):
                conn.send(b"Warning: Cussword detected. Connection terminated.\n")
                print("Cussword detected. Closing connection.")
                break
                
            # Check is there any contact information in the msg
            if contains_contact_info(msg):
                print("Warning send for sharing contact information")
                conn.send(b"Sharing contact info is not allowed!")
                continue
            
            print(f"     Client: {msg}")

            # Replying to Client
            reply = input("You (server): ")
            conn.send(reply.encode())
            if reply.lower() == "bye": 
                print("Closing connection...")
                break

    print("Closing Connection....")
    conn.close()
    server_sock.close()

start_server()