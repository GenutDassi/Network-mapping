
import db_access
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether


async def get_network_info(client_id, network_name):
    query = f"SELECT * FROM network WHERE client_id={client_id} AND network_name={network_name};"
    return await db_access.execute_query(query)


async def create_network(new_network):
    await db_access.execute_query(f"INSERT IGNORE INTO network (client_id, name, location) VALUES {new_network};")
    new_network_id = await db_access.execute_query("SELECT @@IDENTITY AS [@@IDENTITY];")
    return new_network_id


async def create_device(new_device):
    await db_access.execute_query(f"INSERT IGNORE INTO device (ip, mac, network_id) VALUES {new_device};")
    new_device_id = await db_access.execute_query("SELECT @@IDENTITY AS [@@IDENTITY];")
    return new_device_id


async def create_connection(new_connection):
    await db_access.execute_query(f"INSERT IGNORE INTO connection (src_device_id, dst_device_id, protocol) VALUES {new_connection};")
    new_connection_id = await db_access.execute_query("SELECT @@IDENTITY AS [@@IDENTITY];")
    return new_connection_id


# async def add_network(client_id, network_name, network_location, file):
#     network_id = create_network((client_id, network_name, network_location))
#     devices_dict = {}
#     for line in file:
#         src_ip = Ether(line.strip())[IP].src
#         src_mac = Ether(line.strip()).src
#         dst_ip = Ether(line.strip())[IP].dst
#         dst_mac = Ether(line.strip()).dst
#         protocol = "????"  # TODO get the protocol - EXTRA
#         if src_mac not in devices_dict.keys():
#             devices_dict[src_mac] = await create_device((src_ip, src_mac, network_id))
#         if dst_mac not in devices_dict.keys():
#             devices_dict[dst_mac] = await create_device((dst_ip, dst_mac, network_id))
#         src_id = devices_dict[src_mac]
#         dst_id = devices_dict[dst_mac]
#         await create_connection((src_id, dst_id, protocol))
