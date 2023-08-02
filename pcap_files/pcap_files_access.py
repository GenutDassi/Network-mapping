from tkinter import filedialog
from mac_vendor_lookup import AsyncMacLookup
from scapy.all import *
from scapy.layers.inet import IP
from scapy.libs.six import BytesIO

from exception_decorators.catch_exception import catch_exception


@catch_exception
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("PCAP files", "*.pcap")])
    if file_path:
        file = rdpcap(file_path)
        return file
    return None


@catch_exception
def read_pcap_file(pcap_file_content):
    pcap_file = BytesIO(pcap_file_content)
    packets = rdpcap(pcap_file)
    return packets


@catch_exception
def get_src_and_dst_ip_address(packet):
    packet_ip = packet.getlayer(IP)
    if packet_ip:
        src_ip = packet_ip.src
        dst_ip = packet_ip.dst
        return src_ip, dst_ip


@catch_exception
def get_src_and_dst_mac_address(packet):
    src_mac = packet["Ether"].src
    dst_mac = packet["Ether"].dst
    return src_mac, dst_mac


@catch_exception
async def get_vendor_from_mac(mac_address):
    try:
        vendor = await AsyncMacLookup().lookup(mac_address)
        return vendor
    except Exception as e:
        # print("Error:", e)
        # return None
        pass


@catch_exception
def get_protocol(packet):
    if 'TCP' in packet:
        protocol = packet['TCP'].name
    elif 'UDP' in packet:
        protocol = packet['UDP'].name
    elif 'ARP' in packet:
        protocol = packet['ARP'].name
    elif 'ICMP' in packet:
        protocol = packet['ICMP'].name
    else:
        protocol = 'Unknown'
    return protocol
