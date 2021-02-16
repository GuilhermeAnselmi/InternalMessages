import socket

def server_close(host, port):
    host = 'localhost'
    port = 5000
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s.connect((host, port))
    
    code = "73-63-6c-6f-73-65"
    
    s.send(str.encode(str(code)))
    
    s.shutdown(0)
    s.close()