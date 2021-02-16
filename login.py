from tkinter import *
from tkinter import messagebox
from panel import *

class Login:
    def __init__(self, master=None):
        self.access = Frame(master)
        self.access.pack(side=TOP)
        
        self.lblTitle = Label(self.access, text="Entrar em\nInternal Messages", pady="20")
        self.lblTitle.pack(side=TOP)
        
        self.entry = Frame(self.access, pady="10")
        self.entry.pack(side=TOP)
        
        self.lblNome = Label(self.entry, text="Entre com seu nome")
        self.lblNome.grid(row = 0, column = 0)
        
        self.txtName = Entry(self.entry, width="30")
        self.txtName.bind("<Return>", self.logar)
        self.txtName.bind("<Escape>", self.quiting)
        self.txtName.grid(row = 1, column = 0)
        
        self.buttons = Frame(self.access, pady="10")
        self.buttons.pack(side=TOP)
        
        self.btnExit = Button(self.buttons, text="Sair", width="10")
        self.btnExit.bind("<ButtonRelease>", self.quiting)
        #self.btnExit["command"] = self.quiting
        self.btnExit.grid(row = 0, column = 0)
        
        self.aSpace = Label(self.buttons)
        self.aSpace.grid(row = 0, column = 1)
        
        self.btnLogar = Button(self.buttons, text="Entrar", width="10")
        self.btnLogar.bind("<ButtonRelease>", self.logar)
        #self.btnLogar["command"] = self.logar
        self.btnLogar.grid(row = 0, column = 2)
    
    def quiting(self, event):
        log.destroy()
    
    def logar(self, event):
        name = self.txtName.get()
        
        if name != "":
            log.destroy()
            
            window = Tk()
            panel(name, window)
            window.mainloop()
        else:
            messagebox.showwarning(title="Internal Messages", message="Você precisa digitar\nseu nome para entrar")

log = Tk()
Login(log)
log.title("Acesso - IM v1.0")
log.geometry("300x200")
log.resizable(width=False, height=False)
log.mainloop()