from ui import filetransfer
import os

if __name__ == "__main__":
    try:
        filetransfer()
    except KeyboardInterrupt:
        os._exit(0)
