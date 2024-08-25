import socket
import threading
import tkinter as tk
from win10toast import ToastNotifier 
from tkinter import ttk, scrolledtext, simpledialog, messagebox
from plyer import notification


end = 0
saveHost = {'PC': '10.5.76.237', 'TM': '10.5.78.226'}
n = ToastNotifier() 
class ChatGUI:
    def __init__(self, master):
        self.master = master
        
        self.master.title("TCP Chat Application")
        self.master.geometry("500x700")
        self.master.configure(bg='#090909')

        self.chat_label = tk.Label(master, text="Live Server Chat", font=("Helvetica", 14,),bg='#090909',fg='#ffffff')
        self.chat_label.pack(pady=5)

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, font=("Arial", 12,"bold"),bg='#04001c', fg='#ffffff', insertbackground='#ffffff')
        self.text_area.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        self.text_area.config(state=tk.DISABLED)

        self.input_area = tk.Entry(master, font=("Arial", 12),bg='#151515',fg='#ffffff')
        self.input_area.pack(pady=5, padx=10, fill=tk.X, expand=True)
        self.input_area.bind("<Return>", self.write)

        self.send_button = tk.Button(master, text="Send", command=self.write, font=("Arial", 12,'bold'),bg='#151515',fg='white',bd=0,highlightthickness=0)
        self.send_button.pack(pady=5)
        self.nickname = simpledialog.askstring("Nickname", "Choose your nickname:")
        

        self.hostip = simpledialog.askstring("IP Address", "Enter IP Address:")
        self.key = simpledialog.askstring("Password", "Enter password:", show='*')
        self.port = 6000

        if self.hostip in saveHost:
            self.hostip = saveHost[self.hostip]

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.hostip, self.port))
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            self.master.quit()

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        global end
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                elif message == 'PAS':
                    self.client.send(self.key.encode('utf-8'))
                elif message == 'KeyNotFound':
                    end = 1
                    self.text_area.config(state=tk.NORMAL)
                    self.text_area.insert(tk.END, "Wrong key\n")
                    self.text_area.config(state=tk.DISABLED)
                    self.client.close()
                    break
                else: 
                    self.text_area.config(state=tk.NORMAL)
                    self.text_area.insert(tk.END, message + "\n")
                    self.text_area.config(state=tk.DISABLED)
                    self.text_area.yview(tk.END)

                    print(root.state())
                    print("cc")
                    if root.state()=='iconic':
                        notification.notify(
                            title = "TCP CHAT",
                            message = message,
                            timeout = 10
                            )


            except:
                self.text_area.config(state=tk.NORMAL)
                self.text_area.insert(tk.END, "Disconnected\n")
                self.text_area.config(state=tk.DISABLED)
                self.client.close()
                break

    def write(self, event=None):
        global end
        inp = self.input_area.get()
        message = '{}: {}'.format(self.nickname, inp)
        if inp == '/close':
            self.client.send('CLOSE'.encode('utf-8'))
            self.client.close()
            self.master.quit()
        elif inp == '/list':
            self.client.send('LIST'.encode('utf-8'))
        elif inp == '/listname':
            self.client.send('LISTNAME'.encode('utf-8'))
        elif end == 1:
            return
        elif inp.startswith('/msg'):
            parts = inp.split(' ', 2)
            if len(parts) == 3:
                recipient, private_message = parts[1], parts[2]
                message = f'PRIVATE {recipient} {self.nickname}: {private_message}'
                self.client.send(message.encode('utf-8'))
                self.text_area.config(state=tk.NORMAL)
                self.text_area.insert(tk.END, "PRIVATE", "blue_tag")
                self.text_area.insert(tk.END, f" To {recipient}: {private_message}\n")
                self.text_area.tag_configure("blue_tag", foreground="#ff38cd")
                self.text_area.config(state=tk.DISABLED,fg='#ffffff')
                
            else:
                self.text_area.config(state=tk.NORMAL)
                self.text_area.insert(tk.END, "Invalid private message format. Use /msg <recipient> <message>\n")
                self.text_area.config(state=tk.DISABLED)
        elif inp.startswith('/hid'):
            parts = inp.split(' ', 1)
            if len(parts) > 1:
                message = 'Anonymous: {}'.format(parts[1])
                self.client.send(message.encode('utf-8'))
                
            else:
                self.text_area.config(state=tk.NORMAL)
                self.text_area.insert(tk.END, "Message not given\n")
                self.text_area.config(state=tk.DISABLED)
        else:
            self.client.send(message.encode('utf-8'))
        self.input_area.delete(0, tk.END)

# Running the GUI
root = tk.Tk()
gui = ChatGUI(root)
root.mainloop()
