#!/usr/bin/python3

import socket
import time
import threading
from tkinter import *
from tkinter import messagebox


class Client:

    root = None
    host = None
    port = None
    server = None
    online = None
    username = None
    entry = None
    t_lock = None
    thr = None

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(0)

    history = None

    @staticmethod
    def about():
        messagebox.showinfo("About",
                            "Created By Pei Lin Li\t2015\n\n" +
                            "Notes:\n" +
                            "Please type `SHUTDOWN` to turn off the server " +
                            "and use the `Safe Quit` option in the menus to exit"
                            )

    def shutdown(self):
        self.online = False
        self.sock.close()
        self.root.destroy()
        print("----- CONNECTION CLOSED -----")
        sys.exit(0)

    def receiving(self, sock):
        while self.online:
            try:
                self.t_lock.acquire()

                data, address = sock.recvfrom(1024)
                decoded_data = data.decode("utf-8")
                received_message = str(decoded_data)
                self.append_to_history(received_message)
            except OSError:
                pass
            finally:
                self.t_lock.release()

    def sending(self, message):
        if message != "":
            self.sock.sendto(str('\"' + self.username + '\"' + " : " + message).encode("utf-8"), self.server)
            time.sleep(0.2)

    def append_to_history(self, msg):
        if msg != "":
            self.history.configure(state="normal")
            self.history.insert(END, "(" + time.ctime() + ") FROM " + msg + "\n")
            self.history.configure(state="disabled")

    def save_chat_history(self):
        file = open("data.txt", "w")
        self.history.configure(state="normal")
        file.write(self.history.get(0.0, END))
        self.history.configure(state="disabled")
        file.close()

    def load_chat_history(self):
        try:
            file = open("data.txt", "r")
            t = file.read()
            file.close()

            self.history.configure(state="normal")
            self.history.delete(0.0, END)
            self.history.insert(0.0, t)
            self.history.configure(state="disabled")

        except FileNotFoundError:
            print("ERROR: 'data.txt' not found!")

    def get_entry(self, _):
        message = str(self.entry.get())
        self.entry.delete(0, END)
        self.sending(message)

    def draw_menus(self):
        main_menu = Menu(self.root)
        self.root.config(menu=main_menu)

        messaging_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label="Messaging", menu=messaging_menu)
        messaging_menu.add_command(label="Load Chat History", command=self.load_chat_history)
        messaging_menu.add_command(label="Save Chat History", command=self.save_chat_history)
        messaging_menu.add_separator()
        messaging_menu.add_command(label="Quit", command=self.shutdown)

        about_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="About", command=self.about)

    def draw_buttons(self):
        bottom_frame = Frame(self.root)
        bottom_frame.pack()

        connect_btn = Button(bottom_frame, text="CONNECT", command=lambda: self.sending("CONNECT"))
        connect_btn.pack(side=LEFT, pady=5, padx=5)

        self.entry = Entry(bottom_frame, width=25)
        self.entry.pack(side=LEFT, pady=5, padx=5)

        send_btn = Button(bottom_frame, text="SEND", command=lambda: self.get_entry(None))
        send_btn.pack(side=LEFT, pady=5, padx=5)
        self.entry.bind("<Return>", self.get_entry)

    def draw_main_ui(self):
        self.root = Tk()
        self.root.title("Messaging Application")
        self.root.minsize(width=500, height=550)
        self.root.maxsize(width=500, height=550)

        title_frame = Frame(self.root)
        title_frame.pack(fill=X, pady=5, padx=5)
        title = Label(title_frame, text="Python UDP Messaging Application", font="Georgia 14", relief=RIDGE)
        title.pack(fill=X)

        self.history = Text(self.root, height=29, state="disabled")
        self.history.pack(fill=X)

        self.draw_menus()
        self.draw_buttons()

        self.root.mainloop()

        self.online = False
        self.sock.close()
        print("----- CONNECTION CLOSED -----")

    def __init__(self, host, port, server, username):
        print("----- CONNECTION OPENED -----")
        self.host = host
        self.port = port
        self.server = server
        self.username = username
        self.online = True

        self.sock.bind((host, port))
        self.t_lock = threading.Lock()
        self.thr = threading.Thread(target=self.receiving, args=(self.sock,))
        self.thr.start()
        self.draw_main_ui()


class Username:

    root = None
    host = None
    port = None
    server = None

    def __init__(self, host, port, server):
        self.host = host
        self.port = port
        self.server = server

        self.root = Tk()
        self.root.title("Desired Username")
        self.root.minsize(width=200, height=85)

        username_text = Label(self.root, text="Input Desired Username", font="Georgia 12")
        username_text.pack()

        self.username_get = Entry(self.root, width=25, font="Georgia 12")
        self.username_get.pack(pady=5, padx=5)
        self.username_get.bind("<Return>", self.start_main_gui)

        ok_btn = Button(self.root, text="Okay", font="Georgia 10", command=lambda: self.start_main_gui(None))
        ok_btn.pack()

        self.root.mainloop()

    def start_main_gui(self, _):
        username = str(self.username_get.get())
        if username != '':
            self.username_get.delete(0, END)
            self.root.destroy()
            Client(self.host, self.port, self.server, username)


if __name__ == '__main__':
    Username(host="127.0.0.1", port=5500, server=("127.0.0.1", 5000))
