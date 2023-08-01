from fastapi import HTTPException

import network_in_db
import pcap_files_access
import authorization_and_authentication
import technician_in_db


async def login(response, name, password):
    return await authorization_and_authentication.login(response, name, password)


async def signup(name, password):
    return await authorization_and_authentication.signup(name, password)


# TODO: break this module!!
async def add_network(request, client_id, network_name, network_location):
    technician_id = await technician_in_db.get_current_technician()
    if await authorization_and_authentication.check_permission(client_id, technician_id):
        packets = pcap_files_access.upload_file()
        network_id = await network_in_db.create_network((client_id, network_name, network_location))
        devices_dict = {}
        for packet in packets:
            src_mac, dst_mac = pcap_files_access.get_src_and_dst_mac_address(packet)
            if pcap_files_access.get_src_and_dst_ip_address(packet):
                src_ip, dst_ip = pcap_files_access.get_src_and_dst_ip_address(packet)
            src_vendor = pcap_files_access.get_vendor_from_mac(src_mac)
            dst_vendor = pcap_files_access.get_vendor_from_mac(dst_mac)
            protocol = pcap_files_access.get_protocol(packet)
            if src_mac not in devices_dict.keys():
                devices_dict[src_mac] = await network_in_db.create_device((src_ip, src_mac, network_id, src_vendor))
            if dst_mac not in devices_dict.keys():
                devices_dict[dst_mac] = await network_in_db.create_device((dst_ip, dst_mac, network_id, dst_vendor))
            src_id = devices_dict[src_mac]
            dst_id = devices_dict[dst_mac]
            await network_in_db.create_connection((src_id, dst_id, protocol))
        return network_id
    return "error!!!!!!!!!!!!!!!!!!"


async def get_network_information(technician_id, client_id, network_name):
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return network_in_db.get_network_info(client_id, network_name)


async def get_connections(client_id, network_name):
    technician_id = await technician_in_db.get_current_technician()
    # technician_id = authorization_and_authentication.get_current_technician()
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return await network_in_db.get_full_network(client_id, network_name)


async def get_devices(client_id, network_name):
    technician_id = await technician_in_db.get_current_technician()
    # technician_id = authorization_and_authentication.get_current_technician()
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return await network_in_db.get_devices(client_id, network_name)


async def get_devices_by_vendor(client_id, network_name, vendor_name):
    technician_id = await technician_in_db.get_current_technician()
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return await network_in_db.get_devices_by_vendor(client_id, network_name, vendor_name)


async def get_devices_by_mac_address(client_id, network_name, mac_address):
    technician_id = await technician_in_db.get_current_technician()
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return await network_in_db.get_devices_by_mac_address(client_id, network_name, mac_address)
