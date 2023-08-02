from CRUD import network_CRUD, device_CRUD, connections_CRUD
from authorization_and_authentication import authorization_and_authentication
from exception_decorators.catch_exception import catch_exception
from pcap_files import pcap_files_access

@catch_exception
async def get_network_information(current_technician, client_id, network_name):
    if authorization_and_authentication.check_permission(current_technician.id, client_id):
        return await network_CRUD.get_network_info(client_id, network_name)

@catch_exception
async def get_network_connections(current_technician, client_id, network_name):
    if authorization_and_authentication.check_permission(current_technician.id, client_id):
        return await network_CRUD.get_full_network(client_id, network_name)

devices_dict = {}
connections_dict = {}
# the dictionary looks like :
# {(src_mac, dst_mac):{"id": 3, "protocols": "TCP, UDP", "dst_ip":156.890.98.7}}

@catch_exception
async def add_network(current_technician, client_id, network_name, network_location, file_content):
    global devices_dict
    global connections_dict
    devices_dict = {}
    connections_dict = {}
    if await authorization_and_authentication.check_permission(current_technician.id, client_id):
        packets = pcap_files_access.read_pcap_file(file_content)
        network_id = await network_CRUD.create_network(client_id, network_name, network_location)
        for packet in packets:
            src_mac, src_ip, src_vendor, protocol, dst_mac, dst_ip, dst_vendor = await get_packet_info(packet)
            src_id, dst_id = await add_devices(network_id, src_mac, src_ip, src_vendor, dst_mac, dst_ip, dst_vendor)
            await add_connection(src_id, src_mac, dst_ip, dst_id, dst_mac, protocol)
        return network_id
    raise Exception

@catch_exception
async def add_devices(network_id, src_mac, src_ip, src_vendor, dst_mac, dst_ip, dst_vendor):
    global devices_dict
    if src_mac not in devices_dict.keys():
        devices_dict[src_mac] = await device_CRUD.create_device(src_ip, src_mac, network_id, src_vendor)
    if dst_mac not in devices_dict.keys():
        devices_dict[dst_mac] = await device_CRUD.create_device(dst_ip, dst_mac, network_id, dst_vendor)
    src_id = devices_dict[src_mac][0]['last_id']
    dst_id = devices_dict[dst_mac][0]['last_id']
    return src_id, dst_id

@catch_exception
async def add_connection(src_id, src_mac, dst_ip, dst_id, dst_mac, protocol):
    global connections_dict
    dst_ip = update_if_router(src_mac, dst_mac, dst_ip)
    if (src_mac, dst_mac) not in connections_dict.keys():
        connections_dict[(src_mac, dst_mac)] = {
            "connection_id": await connections_CRUD.create_connection(src_id, dst_id, protocol),
            "protocols": protocol,
            "dst_ip": dst_ip
        }
    elif protocol not in connections_dict[(src_mac, dst_mac)]["protocols"]:
        await connections_CRUD.add_protocol_to_connection(
            connections_dict[(src_mac, dst_mac)]["connection_id"],
            protocol)
        connections_dict[(src_mac, dst_mac)]["protocols"] += f", {protocol}"

@catch_exception
async def update_if_router(src_mac, dst_mac, dst_ip):
    if (src_mac, dst_mac) in connections_dict.keys() and \
            dst_ip != connections_dict[(src_mac, dst_mac)]["dst_ip"]:
        return None
    return dst_ip

@catch_exception
async def get_packet_info(packet):
    src_mac, dst_mac = pcap_files_access.get_src_and_dst_mac_address(packet)
    src_ip, dst_ip = pcap_files_access.get_src_and_dst_ip_address(packet)
    src_vendor = await pcap_files_access.get_vendor_from_mac(src_mac)
    dst_vendor = await pcap_files_access.get_vendor_from_mac(dst_mac)
    protocol = pcap_files_access.get_protocol(packet)
    return src_mac, src_ip, src_vendor, protocol, dst_mac, dst_ip, dst_vendor
