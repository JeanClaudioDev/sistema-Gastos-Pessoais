import tkinter as tk

class TopBar(tk.Frame):

    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        usuario = controller.usuario_logado["usuario"]

        label = tk.Label(self, text=f"Usuário: {usuario}")
        label.pack(side="left", padx=10)

        button_logout = tk.Button(self, text="Logout",bg='#1e293b', fg = 'white',
                        command=lambda: self.logout(controller))
        button_logout.pack(side="left")

    def logout(self, controller):
        controller.usuario_logado = None
        controller.mostrar_login()