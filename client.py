import socket as sock

client_sock = sock.socket(sock.AF_INET,sock.SOCK_STREAM)
client_sock.connect(("127.0.0.1",1234))

while True:
    # Authentication process
    msg = client_sock.recv(1024).decode()
    print("Server:", msg, end='')
    
    if "Authentication Failed" in msg:
        print("....Server disconnected..")
        break
            
    if "Authenticated" in msg:
        # Authentication done
        while True:
            # Replying to server
            reply = input("You (Client): ")
            client_sock.send(reply.encode())

            if reply.lower() == "bye":
                print("Closing connection...")
                break

            # Receiving message from the server
            msg = client_sock.recv(512).decode()
            print(f"     Server : {msg}")
            if not msg or msg.lower() == "bye" or msg.startswith("Warning"):
                print("Server disconnected.")
                break
        break

    reply = input("")
    client_sock.send(reply.encode())

            

client_sock.close()
