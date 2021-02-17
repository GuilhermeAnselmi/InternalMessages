import socket

host = 'localhost'
port = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

c = "10"

while c != "0":
    text = input("Msg: ")
    
    if text == "0":
        break
    
    s.sendall(str.encode(str(text)))
    data = s.recv(1024)
    
    print("Mensagem: ", data.decode())
    
s.close()