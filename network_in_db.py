import db_access


async def create_network(new_network):
    await db_access.execute_query("INSERT IGNORE INTO network (client_id, name, location) VALUES (%s, %s, %s);", new_network)
    new_network_id = await db_access.execute_query("SELECT LAST_INSERT_ID();")
    print("id", new_network_id)
    new_network_id = new_network_id[0]["LAST_INSERT_ID()"]
    print("id", new_network_id)
    # last_inserted_id = cursor.fetchone()['last_id']
    # new_network_id = await db_access.execute_query("SELECT @@IDENTITY AS [@@IDENTITY];")
    return new_network_id


async def create_connection(src_id, dst_id, protocol):
    await db_access.execute_query("INSERT IGNORE INTO connection (src_device_id, dst_device_id, protocol) VALUES (%s, %s, %s);",(src_id, dst_id, protocol))
    new_connection_id = await db_access.execute_query("SELECT LAST_INSERT_ID()")
    new_connection_id = new_connection_id[0]["LAST_INSERT_ID()"]
    return new_connection_id


async def get_network_info(client_id, network_name):
    # query = "SELECT * FROM network WHERE client_id=%s AND name=%s;"
    query = "SELECT network.*, client.name FROM (select * FROM network INNER JOIN clients ON " \
            "network.client_id=client.id) WHERE network.client_id=%s AND network.name=%s;"
    return await db_access.execute_query(query, (client_id, network_name))


async def create_device(ip, mac, id, vendor):
    await db_access.execute_query(f"INSERT IGNORE INTO device (network_id, ip, mac, vendor) VALUES (%s, %s, %s, %s);", (id, ip, mac, vendor))
    new_device_id = await db_access.execute_query("SELECT LAST_INSERT_ID() AS last_id;")
    return new_device_id


async def get_devices(client_id, network_name):
    network_id = await db_access.execute_query("SELECT network.id FROM network WHERE client_id=%s AND name=%s;",
                                               (client_id, network_name))
    return await db_access.execute_query(
        "SELECT device.mac, device.ip, device.vendor FROM device WHERE network_id=%s;", network_id)


async def get_full_network(client_id, network_name):
    network_id = await db_access.execute_query("SELECT network.id FROM network WHERE client_id=%s AND network_name=%s;",
                                               (client_id, network_name))
    query = "SELECT * FROM connection INNER JOIN device AS src_device ON connection.src_device_id = src_device.id " \
            "INNER JOIN device AS dst_device ON connection.dst_device_id = dst_device.id WHERE src_device.network_id " \
            "= %s AND dst_device.network_id =%s;"
    return await db_access.execute_query(query, network_id)


async def add_protocol_to_connection(connection_id, protocol):
    previous_protocols = await db_access.execute_query("SELECT protocol FROM connection WHERE id=%s", connection_id)
    previous_protocols = previous_protocols[0]["protocol"]
    uptodate_protocols = f"{previous_protocols}, {protocol}"
    await db_access.execute_query("UPDATE connection SET protocol = %s WHERE id = %s;", (uptodate_protocols, connection_id))
