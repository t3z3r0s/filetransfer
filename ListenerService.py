from tkinter import filedialog
from tkinter import messagebox
import threading
import socket
import struct
import os

class Listen:

    def _startListenAsync(self, port):
        listenerThread = threading.Thread(target=self._listen, args=(port,))
        messagebox.showinfo("Waiting for file", "Listener Thread Started")
        listenerThread.start()
    
    def _listen(self, port):

        try:

            self.serverSocket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.serverSocket.bind(("0.0.0.0", port))
            self.serverSocket.listen()

            connected, address = self.serverSocket.accept()


            def _recv_exact(connection, nrOfBytes):
                decodedData = b""

                while len(decodedData) < nrOfBytes:
                    chunk = connection.recv(nrOfBytes - len(decodedData))
                    if not chunk:
                        raise ConnectionError("Connection Ended")

                    decodedData += chunk

                return decodedData

            file_size, file_format = struct.unpack('>I10s',_recv_exact(connected, 14))

            newFile = filedialog.asksaveasfilename(
                title="Save As:",
                initialdir=os.path.expanduser("~/Downloads"),
                intialfile=f"download{file_format}",
                defaultextesion=f"{file_format}",
                filetypes = [("Text Files", ".txt"), ("All", ".")]
            )

            if not newFile:
                messagebox.showerror("Error", "User didnt save the file.")
                return
    

            with open(newFile, "wb") as f:
                remainingBytes = file_size

                while chunk := connected.recv(min(1024, remainingBytes)):
                    print(chunk)
                    f.write(chunk)
                    remainingBytes -= len(chunk)

            messagebox.showinfo("Success!", "File sent successfully")
            
            
        except OSError as e:
            messagebox.showerror("Error", str(e))

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            messagebox.showinfo("Info", "Ended Listener Connection")



    def _onExitListen(self):

        if self.serverSocket:
            self.serverSocket.close()

