from scapy.layers.inet import IP
from scapy.layers.l2 import Ether

import network_in_db
import pcap_files_access
import authorization_and_authentication
import technician_in_db


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
            src_ip = Ether(packet.strip())[IP].src
            src_mac = Ether(packet.strip()).src
            dst_ip = Ether(packet.strip())[IP].dst
            dst_mac = Ether(packet.strip()).dst
            protocol = "XXXX"  # TODO get the protocol - EXTRA
            if src_mac not in devices_dict.keys():
                devices_dict[src_mac] = await network_in_db.create_device((src_ip, src_mac, network_id))
            if dst_mac not in devices_dict.keys():
                devices_dict[dst_mac] = await network_in_db.create_device((dst_ip, dst_mac, network_id))
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
