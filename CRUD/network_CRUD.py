from DB import db_access


async def create_network(client_id, name, location):
    await db_access.execute_query("INSERT IGNORE INTO network (client_id, name, location) VALUES (%s, %s, %s);", (client_id, name, location))
    new_network_id = await db_access.execute_query("SELECT LAST_INSERT_ID();")
    print("id", new_network_id)
    new_network_id = new_network_id[0]["LAST_INSERT_ID()"]
    print("id", new_network_id)
    # last_inserted_id = cursor.fetchone()['last_id']
    # new_network_id = await db_access.execute_query("SELECT @@IDENTITY AS [@@IDENTITY];")
    return new_network_id


async def get_network_info(client_id, network_name):
    # query = "SELECT * FROM network WHERE client_id=%s AND name=%s;"
    query = "SELECT network.*, client.name FROM (select * FROM network INNER JOIN clients ON " \
            "network.client_id=client.id) WHERE network.client_id=%s AND network.name=%s;"
    return await db_access.execute_query(query, (client_id, network_name))


async def get_full_network(client_id, network_name):
    network_id = await db_access.execute_query("SELECT network.id FROM network WHERE client_id=%s AND network_name=%s;",
                                               (client_id, network_name))
    query = "SELECT * FROM connection INNER JOIN device AS src_device ON connection.src_device_id = src_device.id " \
            "INNER JOIN device AS dst_device ON connection.dst_device_id = dst_device.id WHERE src_device.network_id " \
            "= %s AND dst_device.network_id =%s;"
    return await db_access.execute_query(query, network_id)




