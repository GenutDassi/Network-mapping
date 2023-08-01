from CRUD import technician_CRUD, network_CRUD, device_CRUD, connections_CRUD
from authorization_and_authentication import authorization_and_authentication
from pcap_files import pcap_files_access


# TODO: break this module!!
async def add_network(client_id, network_name, network_location, file_content):
    technician_id = await technician_CRUD.get_current_technician()
    if await authorization_and_authentication.check_permission(client_id, technician_id):
        packets = pcap_files_access.read_pcap_file(file_content)
        network_id = await network_CRUD.create_network(client_id, network_name, network_location)
        devices_dict = {}  # the dictionary looks like : {(src_mac, dst_mac):{"id": 3, "protocols": "TCP, UDP"}}
        connections_dict = {}
        for packet in packets:
            src_mac, dst_mac = pcap_files_access.get_src_and_dst_mac_address(packet)
            if pcap_files_access.get_src_and_dst_ip_address(packet):
                src_ip, dst_ip = pcap_files_access.get_src_and_dst_ip_address(packet)
            src_vendor = pcap_files_access.get_vendor_from_mac(src_mac)
            dst_vendor = pcap_files_access.get_vendor_from_mac(dst_mac)
            protocol = pcap_files_access.get_protocol(packet)
            if src_mac not in devices_dict.keys():
                devices_dict[src_mac] = await device_CRUD.create_device(src_ip, src_mac, network_id, src_vendor)
            if dst_mac not in devices_dict.keys():
                devices_dict[dst_mac] = await device_CRUD.create_device(dst_ip, dst_mac, network_id, dst_vendor)
            src_id = devices_dict[src_mac][0]['last_id']
            dst_id = devices_dict[dst_mac][0]['last_id']
            print("id od src & dst", src_id, src_mac)
            if (src_mac, dst_mac) not in connections_dict.keys():
                connections_dict[(src_mac, dst_mac)] = {
                    "connection_id": await connections_CRUD.create_connection(src_id, dst_id, protocol),
                    "protocols": protocol}
            elif protocol not in connections_dict[(src_mac, dst_mac)]["protocols"]:
                await connections_CRUD.add_protocol_to_connection(
                    connections_dict[(src_mac, dst_mac)]["connection_id"],
                    protocol)
                connections_dict[(src_mac, dst_mac)]["protocols"] += f", {protocol}"
        return "success!!!", network_id
    return "error!!!!!!!!!!!!!!!!!!"


async def get_network_information(technician_id, client_id, network_name):
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return network_CRUD.get_network_info(client_id, network_name)