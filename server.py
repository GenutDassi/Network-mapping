from scapy.layers.inet import IP
from scapy.layers.l2 import Ether

import network_in_db
import pcap_files_access
import authorization_and_authentication
from mac_vendor_lookup import MacLookup
import technician_in_db


def get_src_and_dst_ip_address(packet):
    packet_ip = packet.getlayer(IP)
    if (packet_ip):
        src_ip = packet_ip.src
        dst_ip = packet_ip.dst
        return src_ip, dst_ip


def get_src_and_dst_mac_address(packet):
    src_mac = packet["Ether"].src
    dst_mac = packet["Ether"].dst
    return src_mac, dst_mac


def get_vendor_from_mac(mac_address):
    try:
        vendor = MacLookup().lookup(mac_address)
        return vendor
    except Exception as e:
        # print("Error:", e)
        # return None
        pass


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


async def login(name, password):
    return await authorization_and_authentication.login(name, password)


async def signup(name, password):
    return await authorization_and_authentication.signup(name, password)


async def add_network(technician_id, client_id, network_name, network_location):
    # technician_id = technician_in_db.get_technician_id()
    if authorization_and_authentication.check_permission(client_id, technician_id):
        packets = pcap_files_access.upload_file()
        network_id = network_in_db.create_network((client_id, network_name, network_location))
        devices_dict = {}
        for packet in packets:
            src_mac, dst_mac = get_src_and_dst_mac_address(packet)
            if get_src_and_dst_ip_address(packet):
                src_ip, dst_ip = get_src_and_dst_ip_address(packet)
            src_vendor = get_vendor_from_mac(src_mac)
            dst_vendor = get_vendor_from_mac(dst_mac)
            protocol = get_protocol(packet)
            if src_mac not in devices_dict.keys():
                devices_dict[src_mac] = await network_in_db.create_device((src_ip, src_mac, network_id, src_vendor))
            if dst_mac not in devices_dict.keys():
                devices_dict[dst_mac] = await network_in_db.create_device((dst_ip, dst_mac, network_id, dst_vendor))
            src_id = devices_dict[src_mac]
            dst_id = devices_dict[dst_mac]
            await network_in_db.create_connection((src_id, dst_id, protocol))


async def get_network_information(technician_id, client_id, network_name):
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return network_in_db.get_network_info(client_id, network_name)


async def get_connections(technician_id, client_id, network_name):
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return network_in_db.get_connections(client_id, network_name)


async def get_devices(technician_id, client_id, network_name):
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return network_in_db.get_devices(client_id, network_name)
