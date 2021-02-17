from tkinter import *
from tkinter import messagebox
from panel import *
from clientConfig import *
import os

path = os.path.expanduser("~/")

class Login:
    def __init__(self, master=None):
        #Frame master
        self.access = Frame(master)
        self.access.pack(side=TOP)
        
        #Fontes
        self.fontStyle = tkFont.Font(family="Verdana", size=12, weight="bold")
        
        #Objetos
        self.lblTitle = Label(self.access, text="Entrar em\nInternal Messages", pady="20", font=self.fontStyle)
        self.lblTitle.pack(side=TOP)
        
        self.entry = Frame(self.access, pady="10")
        self.entry.pack(side=TOP)
        
        self.lblNome = Label(self.entry, text="Entre com seu nome")
        self.lblNome.grid(row = 0, column = 0)
        
        self.txtName = Entry(self.entry, width="30")
        self.txtName.bind("<Return>", self.logar)
        self.txtName.bind("<Escape>", self.quiting)
        self.txtName.grid(row = 1, column = 0)
        self.txtName.insert(0, name)
        
        self.check = BooleanVar()
        self.check.set(True)
        
        self.ckbName = Checkbutton(self.entry, text="Salvar Nome", var=self.check)
        self.ckbName.grid(row = 2, column = 0)
        
        self.buttons = Frame(self.access, pady="10")
        self.buttons.pack(side=TOP)
        
        self.btnConfig = Button(self.buttons, text="Configurar", width="12", font="Verdana 10 bold")
        self.btnConfig.bind("<ButtonRelease>", self.config)
        self.btnConfig.grid(row = 1, column = 0)
        
        self.aSpace = Label(self.buttons)
        self.aSpace.grid(row = 1, column = 1)
        
        self.btnLogar = Button(self.buttons, text="Entrar", width="12", font="Verdana 10 bold")
        self.btnLogar.bind("<ButtonRelease>", self.logar)
        self.btnLogar.grid(row = 1, column = 2)
        
        self.btnExit = Button(self.buttons, text="Sair", width="12", font="Verdana 10 bold")
        self.btnExit.bind("<ButtonRelease>", self.quiting)
        self.btnExit.grid(row = 2, column = 0, columnspan = 3)
    
    def quiting(self, event):
        log.destroy()
    
    def logar(self, event):
        name = self.txtName.get()
        host = ""
        port = ""
        
        if name != "":
            if self.check.get():
                try:
                    file = open(path + "clientConfig.config", "r")
                    file.readline()
                    host = file.readline().replace("ip:", "").replace("\n", "")
                    port = file.readline().replace("port:", "")
                    file.close()
                    
                    try:
                        file = open(path + "clientConfig.config", "w")
                        file.writelines("name:" + name + "\n")
                        file.writelines("ip:" + host + "\n")
                        file.writelines("port:" + port)
                        file.close()
                    except:
                        messengebox.showwarning(title="Error - IM", message="Impossible create or modify file clientConfig.config")
                except:
                    file = open(path + "clientConfig.config", "w")
                    file.writelines("name:" + name + "\n")
                    file.writelines("ip:" + host + "\n")
                    file.writelines("port:" + port)
                    file.close()
                finally:
                    log.destroy()
                    
                    window = Tk()
                    panel(name, window)
                    window.mainloop()
                
            else:
                log.destroy()
                
                window = Tk()
                panel(name, window)
                window.mainloop()
        else:
            messagebox.showwarning(title="Internal Messages", message="Você precisa digitar\nseu nome para entrar")
    
    def config(self, event):
        window = Toplevel()
        #window = Tk()
        Client(window)
        window.protocol("WM_DELETE_WINDOW", self.close_win)
        window.transient(log)
        window.focus_force()
        window.grab_set()
        
    def close_win(self):
        self.window.destroy()
        self.window = None

name = ""

try:
    file = open(path + "clientConfig.config", "r")
    name = file.readline().replace("name:", "").replace("\n", "")
    file.close()
except:
    name = ""

log = Tk()
Login(log)
log.title("Acesso - IM v1.4")
log.geometry("300x250+250+250")
log.resizable(width=False, height=False)
log.mainloop()