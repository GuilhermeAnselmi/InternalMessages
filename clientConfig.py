from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import os

path = os.path.expanduser("~/")

host = ""
port = ""

try:
    file = open(path + "clientConfig.config", "r")
    file.readline()
    host = file.readline().replace("ip:", "").replace("\n", "")
    port = file.readline().replace("port:", "")
    file.close()
except:
    host = "localhost"
    port = 0

class Client:
    def __init__(self, master=None):
        def testVal(inStr,acttyp):
            if acttyp == '1': #insert
                if not inStr.isdigit():
                    return False
            return True
        
        #Definição da janela
        self.window = master
        self.window.title("Configurações Iniciais - IM")
        self.window.geometry("300x150+250+250")
        self.window.resizable(width=False, height=False)
        
        #Frame master
        self.container = Frame(master)
        self.container.pack(pady=10, padx=10)
        
        #Frames
        self.conn = LabelFrame(self.container, text="Connection")
        self.conn.pack(side=TOP)
        
        self.buttons = Frame(self.container)
        self.buttons.pack(pady=10, padx=10)
        
        #Objectos
        self.englob = Frame(self.conn)
        self.englob.pack(pady=10, padx=10)
        
        self.lblIp = Label(self.englob, text="IP")
        self.lblIp.grid(row = 0, column = 0)
        
        self.txtIp = Entry(self.englob)
        self.txtIp.grid(row = 0, column = 1)
        
        if host != "localhost":
            self.txtIp.insert(0, host)
        
        self.lblPort = Label(self.englob, text="Port")
        self.lblPort.grid(row = 1, column = 0)
        
        self.txtPort = Entry(self.englob, validate="key")
        self.txtPort["validatecommand"] = (self.txtIp.register(testVal),"%P","%d")
        self.txtPort.grid(row = 1, column = 1)
        
        if port != 0:
            self.txtPort.insert(0, port)
        
        #Buttons
        self.btnDone = Button(self.buttons, text="Done", font="Verdana 10 bold")
        self.btnDone.bind("<ButtonRelease>", self.done)
        self.btnDone.pack(side=LEFT, padx=20)
        
        self.btnSave = Button(self.buttons, text="Save", font="Verdana 10 bold")
        self.btnSave.bind("<ButtonRelease>", self.save)
        self.btnSave.pack(side=RIGHT, padx=20)
    
    def done(self, event):
        self.window.destroy()
    
    def save(self, event):
        name = ""
        
        if self.txtIp.get() != "" and self.txtPort.get() != "":
            try:
                file = open(path + "clientConfig.config", "r")
                name = file.readline().replace("name:", "").replace("\n", "")
                file.close()
                
                try:
                    file = open(path + "clientConfig.config", "w")
                    file.writelines("name:" + name + "\n")
                    file.writelines("ip:" + self.txtIp.get() + "\n")
                    file.writelines("port:" + self.txtPort.get())
                    file.close()
                    self.window.destroy()
                except:
                    messagebox.showwarning(title="Error - IM", message="Impossible create or modify file clientConfig.config")
            except:
                file = open(path + "clientConfig.config", "w")
                file.writelines("name:" + name + "\n")
                file.writelines("ip:" + self.txtIp.get() + "\n")
                file.writelines("port:" + self.txtPort.get())
                file.close()
                self.window.destroy()
        else:
            messagebox.showinfo(title="Failure - IM", message="IP e Porta devem ser preenchidos")

#window = Tk()
#Client(window)
#window.title("Configurações Iniciais - IM")
#window.geometry("300x150")
#window.resizable(width=False, height=False)
#window.mainloop()