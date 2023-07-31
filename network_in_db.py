from pydantic import BaseModel

import db_access


async def get_network_info(client_id, network_name):
    # query = "SELECT * FROM network WHERE client_id=%s AND name=%s;"
    query = "SELECT network.*, client.name FROM (select * FROM network INNER JOIN clients ON " \
            "network.client_id=client.id) WHERE network.client_id=%s AND network.name=%s;"
    return await db_access.execute_query(query, (client_id, network_name))


async def create_network(new_network):
    await db_access.execute_query("INSERT IGNORE INTO network (client_id, name, location) VALUES (%s);", new_network)
    new_network_id = await db_access.execute_query("SELECT @@IDENTITY AS [@@IDENTITY];")
    return new_network_id


async def create_device(new_device):
    await db_access.execute_query(f"INSERT IGNORE INTO device (ip, mac, network_id) VALUES (%s);", new_device)
    new_device_id = await db_access.execute_query("SELECT @@IDENTITY AS [@@IDENTITY];")
    return new_device_id


async def create_connection(new_connection):
    await db_access.execute_query("INSERT IGNORE INTO connection (src_device_id, dst_device_id, protocol) VALUES (%s);",
                                  new_connection)
    new_connection_id = await db_access.execute_query("SELECT @@IDENTITY AS [@@IDENTITY];")
    return new_connection_id


async def get_devices(client_id, network_name):
    network_id = await db_access.execute_query("SELECT network.id FROM network WHERE client_id=%s AND name=%s;",
                                               (client_id, network_name))
    return await db_access.execute_query(
        "SELECT device.mac, device.ip, device.vendor FROM device WHERE network_id=%s;", network_id)


# async def get_connections(client_id, network_name): network_id = await db_access.execute_query("SELECT network.id
# FROM network WHERE client_id=%s AND network_name=%s;", (client_id, network_name)) return await
# db_access.execute_query( "SELECT device.mac, device.id, device.protocol FROM connection WHERE network_id=%s;",
# (network_id))
async def get_full_network(client_id, network_name):
    network_id = await db_access.execute_query("SELECT network.id FROM network WHERE client_id=%s AND network_name=%s;",
                                               (client_id, network_name))
    query = "SELECT * FROM connection INNER JOIN device AS src_device ON connection.src_device_id = src_device.id " \
            "INNER JOIN device AS dst_device ON connection.dst_device_id = dst_device.id WHERE src_device.network_id " \
            "= %s AND dst_device.network_id =%s;"
    return await db_access.execute_query(query, network_id)



class NetworkInfo(BaseModel):
    network_name: str
    location: str
    client_name: str


class Device(BaseModel):
    mac: str
    ip: str
    vendor: str


class Connection(BaseModel):
    protocol: str
    src_device: Device
    dst_device: Device


class Network(BaseModel):
    info: NetworkInfo
    connections: list[Connection]
