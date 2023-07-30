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


async def add_network(client_id, network_name, network_location, path):
    # technician_id = technician_in_db.get_technician_id()
    # if authorization_and_authentication.check_permission(technician_id, client_id):
    # check_permission get technician_id from cookies
    if authorization_and_authentication.check_permission(client_id):
        file = pcap_files_access.upload_file(path)
        network_id = network_in_db.create_network((client_id, network_name, network_location))
        devices_dict = {}
        for line in file:
            src_ip = Ether(line.strip())[IP].src
            src_mac = Ether(line.strip()).src
            dst_ip = Ether(line.strip())[IP].dst
            dst_mac = Ether(line.strip()).dst
            protocol = "????"  # TODO get the protocol - EXTRA
            if src_mac not in devices_dict.keys():
                devices_dict[src_mac] = await network_in_db.create_device((src_ip, src_mac, network_id))
            if dst_mac not in devices_dict.keys():
                devices_dict[dst_mac] = await network_in_db.create_device((dst_ip, dst_mac, network_id))
            src_id = devices_dict[src_mac]
            dst_id = devices_dict[dst_mac]
            await network_in_db.create_connection((src_id, dst_id, protocol))


async def upload_file(client_id, path):
    if await authorization_and_authentication.check_permission(client_id):
        return await pcap_files_access.upload_file(path)


async def network_information(client_id, network_name):
    if await authorization_and_authentication.check_permission(client_id):
        return await network_in_db.get_network_info(client_id, network_name)
