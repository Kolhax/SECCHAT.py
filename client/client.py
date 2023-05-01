import tkinter as tk
import socket
import threading
import select

HOST = input('Ip:  ') # server IP address
PORT = int(input('Port: ')) # server port65432 # server port number

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Chat Room ({HOST}:{PORT}) - Connected To Server")
        self.root.resizable(False, False)
        root.iconbitmap('assets/icon.ico')
        self.create_widgets()
        self.create_socket()
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def create_widgets(self):
        self.text_box = tk.Text(self.root, state="disabled", wrap="word")
        self.text_box.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        self.entry_field = tk.Entry(self.root)
        self.entry_field.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side="right", padx=5, pady=5)

        self.entry_field.bind("<Return>", lambda event: self.send_message())

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        #self.username = input("Enter your username: ")
        #self.sock.sendall(self.username.encode())

    def receive_messages(self):
        """Receive and display messages from the server"""
        while True:
            ready, _, _ = select.select([self.sock], [], [], 1.0)
            if ready:
                data = self.sock.recv(1024)
                if not data:
                    break
                message = data.decode().strip()
                self.display_message(message)

    def send_message(self):
        """Send a message to the server"""
        message = self.entry_field.get().strip()
        if message:
            self.sock.sendall(message.encode())
            self.entry_field.delete(0, tk.END)


    def display_message(self, message):
        """Add a message to the chat window"""
        self.text_box.configure(state="normal")
        self.text_box.insert(tk.END, message + "\n")
        self.text_box.configure(state="disabled")
        self.text_box.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()