from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
import socket
import time, _thread as thread
import threading
from consoleServer import server_close
import os

path = os.path.expanduser("~/")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ender = ""

class Server:
    def __init__(self, master=None):
        def testVal(inStr,acttyp):
            if acttyp == '1': #insert
                if not inStr.isdigit():
                    return False
            return True
        
        #Frame master
        self.container = Frame(master)
        self.container.pack()
        
        #Fontes
        self.fontStyle = tkFont.Font(family="Verdana", size=12, weight="bold")
        
        #Frames de organização
        self.connDef = LabelFrame(self.container, text="Connection Definition")
        self.connDef.grid(row = 0, column = 0, pady=10, padx=10)
        
        self.state = LabelFrame(self.container, text="Status")
        self.state.grid(row = 0, column = 1, pady=10, padx=10)
        
        self.buttons = Frame(self.container)
        self.buttons.grid(row = 0, column = 2, pady=10, padx=10)
        
        self.quant = LabelFrame(self.container, text="Number of Users")
        self.quant.grid(row = 1, column = 0, pady=10, padx=10)
        
        self.save = Frame(self.container)
        self.save.grid(row = 1, column = 2, pady=10, padx=10)
        
        self.log = LabelFrame(self.container, text="Console")
        self.log.grid(row = 2, column = 0, columnspan = 3, pady=10, padx=10)
        
        #Objetos da tela
        #Connection Definition
        self.fm1 = Frame(self.connDef)
        self.fm1.pack(pady=10, padx=10)
        
        self.lblIp = Label(self.fm1, text="IP")
        self.lblIp.grid(row = 0, column = 0, padx=10)
        
        self.lblPort = Label(self.fm1, text="Port")
        self.lblPort.grid(row = 1, column = 0, padx=10)
        
        self.txtIp = Entry(self.fm1)
        self.txtIp.grid(row = 0, column = 1, padx=10)
        
        if host != "localhost":
            self.txtIp.insert(0, host)
        else:
            self.txtIp.insert(0, "")
        
        self.txtPort = Entry(self.fm1, validate="key")
        self.txtPort.insert(0, str(port))
        self.txtPort["validatecommand"] = (self.txtPort.register(testVal), "%P", "%d")
        self.txtPort.grid(row = 1, column = 1, padx=10)
        
        #Status
        self.lblStatus = Label(self.state, fg="red", text="Server: Stopped")
        self.lblStatus.pack(pady=10, padx=10)
        
        #Buttons
        self.btnStart = Button(self.buttons, text="Start", width="10", bg="green", font=self.fontStyle, command=self.init)
        self.btnStart.grid(row = 0, column = 0, pady=5, padx=10)
        
        self.btnStop = Button(self.buttons, text="Stop", width="10", state="disabled", bg="red", font=self.fontStyle, command=self.stopall)
        self.btnStop.grid(row = 1, column = 0, pady=5, padx=10)
        
        #Listen
        self.cmbListen = ttk.Combobox(self.quant, state="readonly")
        self.cmbListen.set(quant)
        self.cmbListen["values"] = ["2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.cmbListen.grid(row = 0, column = 0, pady=10, padx=40)
        
        #Save
        self.btnSave = Button(self.save, text="Save", width="10", bg="green", font=self.fontStyle, command=self.saveFile)
        self.btnSave.grid(row = 0, column = 0)
        
        #Console
        self.lblSpace = Label(self.log)
        self.lblSpace.pack(side=TOP)
        
        #Scrollbar/chat
        self.cs = Scrollbar(self.log, orient="vertical")
        self.cs.pack(side=RIGHT, fill="y")
        
        self.txtConsole = Text(self.log, state="disabled", width="75", height="10", font="Verdana 10", relief="raise", yscrollcommand=self.cs.set)
        self.txtConsole.pack(side=BOTTOM)
        
        self.cs.config(command=self.txtConsole.yview)
    
    def now(self):
        return time.ctime(time.time())
    
    def broadcast(self, msg):
        for client in clients:
            clients[client].send(msg)
    
    def client(self, conn, posi):
        name = ""
        
        while True:
            data = conn.recv(1024)
            
            if len(data) < 17 and len(data) != 0:
                self.txtConsole["state"] = "normal"
                self.txtConsole.insert(END, "Error receiving data\n\n")
                self.txtConsole.yview_moveto(1.0)
                self.txtConsole["state"] = "disabled"
            else:                
                code = data.decode("utf8")[:17]
                msg = data.decode("utf8")[17:]
                
                print(str(code) + "\n")
                print(str(msg))
                
                if code == "00-00-6e-61-6d-65":
                    name = str(msg)
                    msg = str(msg) + " is connected\n\n"
                    self.broadcast(msg.encode())
                    
                    consoleMsg = str(code) + "_" + str(msg)
                    self.txtConsole["state"] = "normal"
                    self.txtConsole.insert(END, consoleMsg)
                    self.txtConsole["state"] = "disabled"
                elif code == "73-63-6c-6f-73-65":
                    #server close
                    c = 0
                elif code == "63-63-6c-6f-73-65":
                    self.txtConsole["state"] = "normal"
                    self.txtConsole.insert(END, name + " closed the connection\n\n")
                    self.txtConsole["state"] = "disabled"
                elif code == "00-00-00-00-00-00":
                    self.broadcast(msg.encode())
                    
                    consoleMsg = str(code) + "_" + str(msg)
                    self.txtConsole["state"] = "normal"
                    self.txtConsole.insert(END, consoleMsg)
                    self.txtConsole["state"] = "disabled"
                    
                self.txtConsole.yview_moveto(1.0)
                
                if not data:
                    clients.pop(posi)
                    conn.close()
                    break
        
        conn.close()
    
    def run(self):
        try:
            s.bind((host, port))
            s.listen(quant)
            
            self.txtConsole["state"] = "normal"
            self.txtConsole.insert(END, "Server is running\n")
            self.txtConsole.yview_moveto(1.0)
            self.txtConsole["state"] = "disabled"
        except:
            self.txtConsole["state"] = "normal"
            self.txtConsole.insert(END, "Server running with errors\n")
            self.txtConsole.insert(END, "s.bind((" + str(host) + ", " + str(port) +
                                   ")) or s.listen(" + str(quant) + ") it's not correct\n\n")
            self.txtConsole.yview_moveto(1.0)
            self.txtConsole["state"] = "disabled"
        finally:
            self.lblStatus["text"] = "Server: Running"
            self.lblStatus["fg"] = "green"
            self.btnStop["state"] = "normal"
            
            self.txtConsole["state"] = "normal"
            self.txtConsole.insert(END, "Waiting for Connection...\n\n")
            self.txtConsole.yview_moveto(1.0)
            self.txtConsole["state"] = "disabled"
            
            cont = 0
            
            while True:
                conn, ender = s.accept()
                
                code = conn.recv(1024)
                
                if code.decode() == "73-63-6c-6f-73-65":
                    #conn.close()
                    break
                
                self.txtConsole["state"] = "normal"
                self.txtConsole.insert(END, "Connected in " + str(ender) + " at " + str(self.now()) + "\n\n")
                self.txtConsole.yview_moveto(1.0)
                self.txtConsole["state"] = "disabled"
        
                clients[cont] = conn
                
                thread.start_new_thread(self.client, (conn, cont,))
                
                cont += 1
            
    def stopall(self):
        self.btnStop["state"] = "disabled"
        
        code = "73-63-6c-6f-73-65"
        
        self.broadcast(code.encode())
        
        #chamar consoleServer.py
        server_close(host, port)
        
        time.sleep(2)
        
        #start_new_thread.stop()
        #Thread.stop()
        #s.shutdown(0)
        #s.close()
        
        self.txtConsole["state"] = "normal"
        self.txtConsole.insert(END, "Server stopped\n\n")
        self.txtConsole.yview_moveto(1.0)
        self.txtConsole["state"] = "disabled"
        
        self.lblStatus["text"] = "Server: Stopped"
        self.lblStatus["fg"] = "red"
        self.btnStart["state"] = "normal"
    
    def init(self):
        self.btnStart["state"] = "disabled"
        threading.Thread(target=self.run).start()
        
    def saveFile(self):
        file = open(path + "initial.config", "w")
        if self.txtIp.get() != "" :
            file.write("ip:" + self.txtIp.get() + "\n")
        else:
            file.write("ip:localhost\n")
        
        if self.txtPort.get() != "":
            file.write("port:" + self.txtPort.get() + "\n")
        else:
            file.write("port:5000\n")
        
        file.write("listen:" + self.cmbListen.get())
        file.close()

clients = {}
host = 'localhost'
port = 50000
quant = 5
#threading.Thread(target=stopall).start()
#run()

try:
    file = open(path + "initial.config", "r")
    host = file.readline().replace("ip:", "").replace("\n", "")
    port = int(file.readline().replace("port:", "").replace("\n", ""))
    quant = int(file.readline().replace("listen:", ""))
    file.close()
except:
    file = open(path + "initial.config", "a")
    file.write("ip:localhost\n")
    file.write("port:5000\n")
    file.write("listen:5")
    file.close()

window = Tk()
Server(window)
window.title("Server - IM v1.5")
window.resizable(width=False, height=False)
window.geometry("650x420")
#window.minsize(width=600, height=400)
#window.maxsize(width=620, height=420)
window.mainloop()