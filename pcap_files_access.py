from tkinter import filedialog
from scapy.all import rdpcap

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("PCAP files", "*.pcap")])
    if file_path:
        file = rdpcap(file_path)
        return file
    return None


def read_file(path):
    pass
