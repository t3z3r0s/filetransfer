from tkinter import messagebox
import threading
import socket
import struct
import os

class Send:


    def _startSendAsync(self, senderName, targetIP, port, file_format, file):
        listenerThread = threading.Thread(target=self._send, args=(senderName, targetIP,
                                                                   port, file_format,
                                                                   file)
        )
        messagebox.showinfo("Waiting for file", "Sender Thread Started")
        listenerThread.start()

    
    def _send(self, senderName, targetIP, port, file_format, file):
        
        if not senderName or not targetIP or not port or not file_format or file is None:
            return

        try:
            print(senderName, targetIP, port, file_format, file)

            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            clientSocket.connect((targetIP, port))


            file_header = struct.pack('>I10s',
                                      os.path.getsize(file),
                                      file_format.encode()
            )

            clientSocket.sendall(
                file_header
            )
            
            try:
                with open(f"{file}", "rb") as f:

                    while chunk := f.read(1024):
                        clientSocket.sendall(chunk)


                clientSocket.shutdown(socket.SHUT_WR)

            except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
                messagebox.showerror("File Read Error", e)
            except OSError as e:
                messagebox.showerror("Default OS Error", e)
            except Exception as e:
                messagebox.showerror("Unamed Exception", e)

        except (ConnectionRefusedError, ConnectionResetError,BrokenPipeError, TimeoutError) as e:
            messagebox.showerror("Socket Error", e)

        except Exception as e:
            messagebox.showerror("Oops...", f"Unknown Error: {e}")
            
