import socket
import time
import threading
from tkinter import *
from tkinter import messagebox

received_message = ""
shutdown = False

host = "127.0.0.1"
port = 0
server = ("127.0.0.1", 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

username = "Default"


def update_messages_sent():
    if received_message != "":
        messages_sent.configure(state="normal")
        messages_sent.insert(END, received_message + "\n    (" + time.ctime() + ")\n")
        messages_sent.configure(state="disabled")


def main_shutdown():
    global shutdown
    shutdown = True
    s.close()
    root.destroy()
    print("----- CONNECTION ENDED -----")


class Client:
    def __init__(self):
        self.t_lock = threading.Lock()

        self.t = threading.Thread(target=self.receiving, args=(s, ))
        self.t.start()

        print("----- CONNECTION STARTED -----")

    def receiving(self, sock):
        while not shutdown:
            try:
                self.t_lock.acquire()
                while True:
                    data, address = sock.recvfrom(1024)
                    decoded_data = data.decode("utf-8")
                    global received_message
                    received_message = str(decoded_data)
                    update_messages_sent()
            except OSError:
                pass
            finally:
                self.t_lock.release()

    def sending(self, message):
        if message != "":
            s.sendto(str(username + ": " + message).encode("utf-8"), server)
            time.sleep(0.2)


class Buttons:
    def __init__(self, master):
        bottom_frame = Frame(master)
        bottom_frame.pack()

        self.refresh_btn = Button(bottom_frame, text="REFRESH", command=update_messages_sent)
        self.refresh_btn.pack(side=LEFT, pady=5, padx=5)

        self.entry = Entry(bottom_frame, width=25)
        self.entry.pack(side=LEFT, pady=5, padx=5)

        self.send_btn = Button(bottom_frame, text="SEND", command=lambda: self.get_entry(None))
        self.send_btn.pack(side=LEFT, pady=5, padx=5)
        self.entry.bind("<Return>", self.get_entry)

        self.run_client = Client()

    def get_entry(self, event):
        x = str(self.entry.get())
        self.entry.delete(0, END)
        self.run_client.sending(x)


# noinspection PyMethodMayBeStatic
class Menus:
    def __init__(self, master):
        main_menu = Menu(master)
        master.config(menu=main_menu)

        messaging_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label="Messaging", menu=messaging_menu)
        messaging_menu.add_command(label="Load Chat History", command=self.load_chat_history)
        messaging_menu.add_command(label="Save Chat History", command=self.save_chat_history)
        messaging_menu.add_separator()
        messaging_menu.add_command(label="Safe Quit", command=main_shutdown)

        about_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="About", command=self.about)

    def save_chat_history(self):
        file = open("User_Data.txt", "w")
        messages_sent.configure(state="normal")
        file.write(messages_sent.get(0.0, END))
        messages_sent.configure(state="disabled")
        file.close()

    def load_chat_history(self):
        messages_sent.configure(state="normal")
        messages_sent.delete(0.0, END)
        file = open("User_Data.txt", "r")
        t = file.read()
        messages_sent.insert(0.0, t)
        messages_sent.configure(state="disabled")
        file.close()

    def about(self):
        messagebox.showinfo("About", "Created By Pei Lin Li\n2015")

class MainGUI:
    def __init__(self):
        global root
        root = Tk()
        root.title("Messaging Application")
        root.minsize(width=500, height=550)
        root.maxsize(width=500, height=550)

        title_frame = Frame(root)
        title_frame.pack(fill=X, pady=5, padx=5)
        title = Label(title_frame, text="--- TARGET USER ---", font="Georgia 14", relief=RIDGE)
        title.pack(fill=X)

        global messages_sent
        messages_sent = Text(root, height=29, state="disabled")
        messages_sent.pack(fill=X)

        self.run_menus = Menus(root)
        self.run_buttons = Buttons(root)

        root.mainloop()


class UsernameGUI:
    def __init__(self):
        self.username_root = Tk()
        self.username_root.title("Desired Username")
        self.username_root.minsize(width=200, height=85)

        username_text = Label(self.username_root, text="Input Desired Username", font="Georgia 12")
        username_text.pack()

        self.username_get = Entry(self.username_root, width=25, font="Georgia 12")
        self.username_get.pack(pady=5, padx=5)
        self.username_get.bind("<Return>", self.start_main_gui)

        ok_btn = Button(self.username_root, text="Okay", font="Georgia 10", command=lambda: self.start_main_gui(None))
        ok_btn.pack()

        self.username_root.mainloop()

    def start_main_gui(self, event):
        d_username = str(self.username_get.get())
        global username
        username = d_username
        self.username_get.delete(0, END)
        self.username_root.destroy()
        run_main_gui = MainGUI()

start = UsernameGUI()
