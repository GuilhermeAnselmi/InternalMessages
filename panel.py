from tkinter import *
from tkinter import messagebox
import socket
import threading
import os
import time

path = os.path.expanduser("~/")

host = 'localhost'
port = 0    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class panel:
    def __init__(self, name="Dev", master=None):
        try:
            file = open(path + "clientConfig.config", "r")
            file.readline()
            host = file.readline().replace("ip:", "").replace("\n", "")
            port = int(file.readline().replace("port:", ""))
            file.close()
            print(host)
            print(port)
        except:
            host = 'localhost'
            port = 5000
        
        self.name = name
        #self.name = "Teste"
        self.th = False
        
        #Declarando os parametros da janela
        self.window = master
        self.window.title("Internal Messages v1.5")
        self.window.geometry("800x630+50+50")
        #self.window.minsize(width=800, height=600)
        #self.window.maxsize(width=800, height=660)
        self.window.resizable(width=False, height=False)
        
        try:
            s.connect((host, port))
            s.send(str.encode(str("00-00-00-00-00-00")))
            time.sleep(1.5)
            s.send(str.encode(str("00-00-6e-61-6d-65" + self.name)))
        except:
            messagebox.showwarning(title="Internal Message Error", message="Error Code: 503\nServidor não encontrado")
            self.window.destroy()
        
        #Frame mestre da janela
        self.container = Frame(master, pady="20")
        self.container.pack(side=TOP)
        
        #Frames de containers secundarios
        self.title = LabelFrame(self.container, text="Logado como")
        self.title.pack(side=TOP, fill="both", expand="yes", padx=20, pady=10)
        
        self.chatA = LabelFrame(self.container, text="Chat")
        self.chatA.pack(side=TOP, fill="both", expand="yes", padx=20, pady=10)
        
        self.chat = Frame(self.chatA)
        self.chat.pack(padx=10, pady=10)
        
        self.msg = LabelFrame(self.container, text="Digite sua mensagem")
        self.msg.pack(side=TOP, fill="both", expand="yes", padx=20, pady=10)
        
        self.quit = Frame(self.container)
        self.quit.pack(side=TOP, fill="both", expand="yes", padx=20, pady=10)
        
        #Nome so usuário
        self.lblLogado = Label(self.title, text=self.name, font="Verdana 12 bold")
        self.lblLogado.pack(side=LEFT, padx=40)
        
        #Scrollbar/chat
        self.cs = Scrollbar(self.chat, orient="vertical")
        self.cs.pack(side=RIGHT, fill="y")
        
        self.txtChat = Text(self.chat, width="80", height="20", font="Verdana 10 bold", state="disabled", relief="raise", yscrollcommand=self.cs.set)
        self.txtChat.bind("<Escape>", self.quiting)
        self.txtChat.pack(side=RIGHT)
        
        self.cs.config(command=self.txtChat.yview)
        
        #Escrever a mensagem para envio       
        self.txtMsg = Entry(self.msg, width="70")
        self.txtMsg.bind("<Return>", self.send)
        self.txtMsg.bind("<Escape>", self.quiting)
        self.txtMsg.pack(side=LEFT)
        
        #Botões
        self.btnSend = Button(self.msg, text="Enviar", width="10", height="2", font="Verdana 12 bold")
        self.btnSend.bind("<Button>", self.send)
        self.btnSend.pack(side=RIGHT)
        
        self.btnExit = Button(self.quit, text="Sair", width="10", font="Verdana 10 bold")
        self.btnExit.bind("<Button>", self.quiting)
        self.btnExit.grid(row = 3, column = 0, columnspan = 3)
        
        def request():
            while True:
                data = s.recv(1024)
                
                msg = data.decode()
                
                if msg == "73-63-6c-6f-73-65":
                    th = True
        
                    s.send(str.encode(str("63-63-6c-6f-73-65" + self.name)))
                    
                    s.shutdown(0)
                    s.close()
                    self.window.destroy()
                    break
                    
                #print(msg)
                self.txtChat["state"] = "normal"
                self.txtChat.insert(END, msg)
                self.txtChat.yview_moveto(1.0)
                self.txtChat["state"] = "disabled"
    
        threading.Thread(target=request).start()
        
        if self.th:
            threading.stop()
    
    def quiting(self, event):
        th = True
        
        s.send(str.encode(str("63-63-6c-6f-73-65" + self.name)))
        
        s.shutdown(0)
        s.close()
        self.window.destroy()
    
    def send(self, event):
        msg = str(self.txtMsg.get())
        
        if msg != "":
            msg = "00-00-00-00-00-00" + self.name + ":\n  " + msg + "\n\n"
            
            s.send(str.encode(str(msg)))
            
            self.txtMsg.delete(0, END)
        
    


#window = Tk()
#panel(window)
#window.title("Internal Messages v1.5")
#window.geometry("800x600")
#window.resizable(width=False, height=False)
#window.mainloop()