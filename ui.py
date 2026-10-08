import tkinter as tk
from tkinter import filedialog
from SendService import Send
from ListenerService import Listen

class filetransfer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.resizable(False,False)
        self.geometry("400x150")
        self.title("filetransfer")
        self.config(bg="white")


        self.sendManager = Send()
        self.listenManager = Listen()

        _mainmenu = tk.Menu(self)
        _mainmenu.add_command(label = "Send",    command=self._sendFrame)  
        _mainmenu.add_command(label = "Recieve", command=self._recieveFrame)
        _mainmenu.add_command(label = "Exit",    command=self.destroy)
        _mainmenu.add_command(label = "                         filetransfer", state="disabled")
        self.config(menu=_mainmenu)


        self.__loadMainUI()
        self.mainloop()

    def __loadMainUI(self):

        self.sendUIFrame = tk.Frame(self, bg="white", width=400, height=150)
        self.sendUIFrame.place(x=0, y=0, anchor="nw")

        self.recieveUIFrame = tk.Frame(self, bg="white", width=400, height=150)
        self.recieveUIFrame.place(x=0, y=0, anchor="nw")


        self._sendFrame()

        
        
    def _sendFrame(self):
        self.recieveUIFrame.place_forget()
        self.sendUIFrame.place(x=0,y=0,anchor="nw")
        self._loadSenderUI()

    def _recieveFrame(self):
        self.sendUIFrame.place_forget()
        self.recieveUIFrame.place(x=0,y=0,anchor="nw")
        self._loadRecieveUI()

    def _loadRecieveUI(self):
        self.port = tk.StringVar(value="5050")
        
        _port_label = tk.Label(self.recieveUIFrame, text="Enter Listener Port:", font=("Courier New", 8), bg="white").place(x=20, y=5, anchor="nw")
        _port_entry = tk.Entry(self.recieveUIFrame, textvariable=self.port).place(x=20, y=20, anchor="nw")

        _recieved_history_label = tk.Label(self.recieveUIFrame, text="Recieved History:", font=("Courier New", 8), bg="white").place(x=380, y=5, anchor="ne")
    
        _receivedObjectsFrame = tk.Canvas(self.recieveUIFrame, height=112, width=145, relief="ridge", borderwidth=2); _receivedObjectsFrame.place(x=365, y=20, anchor="ne")
        _scrollbar = tk.Scrollbar(self.recieveUIFrame, orient="vertical", command=_receivedObjectsFrame.yview); _scrollbar.place(x=380, y=20, height=115, anchor="ne")
        _receivedObjectsFrame.configure(yscrollcommand=_scrollbar.set)


        _listen_btn = tk.Button(self.recieveUIFrame, text="Listen:", width=17,command=lambda: self.listenManager._startListenAsync(
                int(self.port.get())
            ))
        _listen_btn.place(x=20, y=105, anchor="nw")


    def _loadSenderUI(self):
        self.sender_name = tk.StringVar(value="anon")
        self.target_ip = tk.StringVar(value="127.0.0.1")
        self.port = tk.StringVar(value="5050")
        self.file_format = tk.StringVar(value=".txt")
        self.file        = None

       
        _sender_name_label = tk.Label(self.sendUIFrame, text="Enter Sender Name:", font=("Courier New", 8), bg="white").place(x=20, y=5, anchor="nw")
        _sender_name_entry = tk.Entry(self.sendUIFrame, textvariable=self.sender_name).place(x=20, y=20, anchor="nw")

        _sender_ip_label = tk.Label(self.sendUIFrame, text="Enter File Format:", font=("Courier New", 8), bg="white").place(x=20, y=55, anchor="nw")
        _sender_ip_entry = tk.Entry(self.sendUIFrame, textvariable=self.file_format).place(x=20, y=70, anchor="nw")

        
        _port_label = tk.Label(self.sendUIFrame, text="Enter Port:", font=("Courier New", 8), bg="white").place(x=380, y=5, anchor="ne")
        _port_entry = tk.Entry(self.sendUIFrame, textvariable=self.port).place(x=380, y=20, anchor="ne")

        _target_ip_label = tk.Label(self.sendUIFrame, text="Enter Target IP:", font=("Courier New", 8), bg="white").place(x=380, y=55, anchor="ne")
        _target_ip_entry = tk.Entry(self.sendUIFrame, textvariable=self.target_ip).place(x=380, y=70, anchor="ne")


        _file_button = tk.Button(self.sendUIFrame, text="Select File:",font=(None, 8), command=self._selectFile).place(x=380, y=105, anchor="ne")

        _send_btn = tk.Button(self.sendUIFrame, text="Send:", width=17,command=lambda: self.sendManager._startSendAsync(
                str(self.sender_name.get()),
                str(self.target_ip.get()),
                int(self.port.get()),
                str(self.file_format.get()),
                self.file
            ))
        _send_btn.place(x=20, y=105, anchor="nw")          

    def _selectFile(self):
        self.file = filedialog.askopenfilename()
        print(self.file)

