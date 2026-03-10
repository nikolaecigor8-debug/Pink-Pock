import json  # for saving servers to a file
from customtkinter import *

class Launcher(CTk):
    def __init__(self):
        super().__init__()

        self.geometry("400x600")
        self.top = CTkFrame(self)
        self.bottom = CTkFrame(self)

        CTkLabel(self.top, text="Server name").pack()
        self.server_name = CTkEntry(self.top)
        self.server_name.pack()

        CTkLabel(self.top, text="Server ip").pack()
        self.server_ip = CTkEntry(self.top)
        self.server_ip.pack()

        CTkLabel(self.top, text="Server port").pack()
        self.server_port = CTkEntry(self.top)
        self.server_port.pack()

        self.save_server_btn = CTkButton(self.top, text="Save server", command=self.save_server)
        self.save_server_btn.pack()
        self.remove_server_btn = CTkButton(self.top, text="remove server", command=self.remove_server)
        self.remove_server_btn.pack()

        self.server_id = 0
        self.current_server_id = 0
        self.servers = []

        CTkLabel(self.top, text="Nickname:").pack()
        self.nickname = CTkEntry(self.top)
        self.nickname.pack()

        self.top.pack()
        self.bottom.pack()

    def load_servers(self):
        try:
            with open("servers.json", "r") as f:
                self.servers = json.load(f)
        except FileNotFoundError:
            self.servers = []

    def show_servers(self):
        # Очищуємо нижню панель перед відображенням
        for child in self.bottom.winfo_children():
            child.destroy()
            
        for server in self.servers:
            CTkLabel(self.bottom, text=server['name']).pack()
            CTkButton(self.bottom, text="Chose", 
                      command=lambda server_id=server['id']: self.chose_server(server_id)).pack()

    def chose_server(self, server_id):
        self.current_server_id = server_id

        self.server_name.delete(0, 'end')
        self.server_ip.delete(0, 'end')
        self.server_port.delete(0, 'end')

        # Пошук сервера за id
        target_server = next((s for s in self.servers if s['id'] == server_id), None)
        if target_server:
            self.server_name.insert(0, target_server["name"])
            self.server_ip.insert(0, target_server["ip"])
            self.server_port.insert(0, target_server["port"])

    def remove_server(self):
        # Видаляємо сервер за поточним id
        self.servers = [s for s in self.servers if s['id'] != self.current_server_id]
        with open("servers.json", 'w') as f:
            json.dump(self.servers, f, indent=4)
        self.show_servers()

    def save_server(self):
        server = {
            "id": self.server_id,
            "name": self.server_name.get(),
            "ip": self.server_ip.get(),
            "port": self.server_port.get()
        }

        # Оновлення існуючого або додавання нового
        self.servers.append(server)
        
        with open("servers.json", "w") as f:
            json.dump(self.servers, f, indent=4)

        self.server_id += 1
        self.show_servers()

if __name__ == "__main__":
    app = Launcher()
    app.load_servers()
    app.show_servers()
    app.mainloop()