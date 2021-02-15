import socket
import time, _thread as thread
import threading
import sys

host = 'localhost'
port = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(10)

def agora():
    return time.ctime(time.time())

def broadcast(msg):
    for client in clients:
        clients[client].send(msg)

def client(conn, posi):
    time.sleep(5)
    
    while True:
        data = conn.recv(1024)
        
        print(data.decode("utf8"))
        
        if not data:
            clients.pop(posi)
            #clients.remove(conn)
            break
        
        #conn.send(bytes(data, "utf8"))
        
        broadcast(data)
    
    print("Fechando conexão")
    conn.close()

def run():
    print("Aguardando conexão...")
    
    cont = 0
    
    while True:
        conn, ender = s.accept()
        print("Conectado em ", ender, end=' ')
        print('as ', agora())

        clients[cont] = conn
        
        thread.start_new_thread(client, (conn, cont,))
        
        cont += 1
        
def stopall():
    running = input("Digite 0 para matar a execução > ")
    
    if running == 0:
        threading.stop()
        quit()
    
clients = {}
threading.Thread(target=stopall).start()
run()