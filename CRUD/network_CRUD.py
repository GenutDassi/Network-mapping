from DB import db_access
from exception_decorators.catch_exception import catch_exception


# @catch_exception
async def create_network(client_id, name, location):
    await db_access.execute_query("INSERT IGNORE INTO network (client_id, name, location) VALUES (%s, %s, %s);",
                                  (client_id, name, location))
    new_network_id = await db_access.execute_query("SELECT LAST_INSERT_ID();")
    new_network_id = new_network_id[0]["LAST_INSERT_ID()"]
    return new_network_id


# @catch_exception
async def get_network_info(client_id, network_name):
    query = "SELECT network.name, network.location, client.FirstName, client.LastName FROM network INNER JOIN client " \
            "WHERE network.client_id = client.id AND network.name = %s AND client.id = %s;"
    return await db_access.execute_query(query, (network_name, client_id))


# @catch_exception
async def get_full_network(client_id, network_name):
    network_id = await db_access.execute_query("SELECT network.id FROM network WHERE client_id=%s AND name=%s;",
                                               (client_id, network_name))
    query = "SELECT src_device.mac AS src_mac, src_device.ip AS src_ip, src_device.vendor AS src_vendor, " \
            "connection.protocol,dst_device.mac AS dst_mac, dst_device.ip AS dst_ip, dst_device.vendor AS dst_vendor " \
            "FROM connection INNER JOIN device AS src_device ON connection.src_device_id = src_device.id INNER JOIN " \
            "device AS dst_device ON connection.dst_device_id = dst_device.id WHERE src_device.network_id = %s AND " \
            "dst_device.network_id = %s;"
    network_id = network_id[0]["id"]
    return await db_access.execute_query(query, (network_id, network_id))
