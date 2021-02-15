from tkinter import *
from tkinter import messagebox
import socket
import threading

host = 'localhost'
port = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class panel:
    def __init__(self, name="Dev", master=None):
        self.name = name
        #self.name = "Teste"
        self.th = False
        
        #Declarando os parametros da janela
        self.window = master
        self.window.title("Internal Messages v0.3")
        self.window.geometry("800x600")
        self.window.resizable(width=False, height=False)
        
        try:
            s.connect((host, port))
            messagebox.showinfo(title="Internal Message", message="Bem-Vindo " + self.name)
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
        self.lblLogado = Label(self.title, text=self.name)
        self.lblLogado.pack(side=LEFT, padx=40)
        
        #Scrollbar/chat
        self.cs = Scrollbar(self.chat, orient="vertical")
        self.cs.pack(side=RIGHT, fill="y")
        
        self.txtChat = Text(self.chat, width="80", height="20", state="disabled", relief="raise", yscrollcommand=self.cs.set)
        self.txtChat.bind("<Escape>", self.quiting)
        #self.txtChat.grid(row = 2, column = 0, columnspan = 2)
        self.txtChat.pack(side=RIGHT)
        
        self.cs.config(command=self.txtChat.yview)
        
        #Escrever a mensagem para envio       
        self.txtMsg = Entry(self.msg, width="70")
        self.txtMsg.bind("<Return>", self.send)
        self.txtMsg.bind("<Escape>", self.quiting)
        self.txtMsg.pack(side=LEFT)
        
        #Botões
        self.btnSend = Button(self.msg, text="Enviar", width="10", height="2")
        self.btnSend.bind("<Button>", self.send)
        self.btnSend.pack(side=RIGHT)
        
        self.btnExit = Button(self.quit, text="Sair", width="10")
        self.btnExit.bind("<Button>", self.quiting)
        self.btnExit.grid(row = 3, column = 0, columnspan = 3)
        
        def request():
            while True:
                data = s.recv(1024)
                
                msg = data.decode()
                print(msg)
                self.txtChat["state"] = "normal"
                self.txtChat.insert(END, msg)
                self.txtChat.yview_moveto(1.0)
                self.txtChat["state"] = "disabled"
    
        threading.Thread(target=request).start()
        
        if self.th:
            threading.stop()
    
    def quiting(self, event):
        th = True
        
        s.shutdown(1)
        s.close()
        self.window.destroy()
    
    def send(self, event):
        msg = str(self.txtMsg.get())
        msg = self.name + ":\n  " + msg + "\n"
        
        s.send(str.encode(str(msg)))
        
        self.txtMsg.delete(0, END)
        
    


#window = Tk()
#panel(window)
#window.title("Internal Messages v0.3")
#window.geometry("800x600")
#window.resizable(width=False, height=False)
#window.mainloop()