from DB import db_access


async def create_device(ip, mac, id, vendor):
    await db_access.execute_query(f"INSERT IGNORE INTO device (network_id, ip, mac, vendor) VALUES (%s, %s, %s, %s);",
                                  (id, ip, mac, vendor))
    new_device_id = await db_access.execute_query("SELECT LAST_INSERT_ID() AS last_id;")
    return new_device_id


async def get_devices(client_id, network_name):
    network_id = await db_access.execute_query("SELECT network.id FROM network WHERE client_id=%s AND name=%s;",
                                               (client_id, network_name))
    return await db_access.execute_query(
        "SELECT device.mac, device.ip, device.vendor FROM device WHERE network_id=%s;", network_id)


async def get_devices_by_vendor(client_id, network_name, vendor_name):
    network_id = await db_access.execute_query("SELECT network.id FROM network WHERE client_id=%s AND name=%s;",
                                               (client_id, network_name))
    return await db_access.execute_query(
        "SELECT device.mac, device.ip, device.vendor FROM device WHERE network_id=%s AND vendor = %s;",
        (network_id, vendor_name))


async def get_devices_by_mac_address(client_id, network_name, mac_address):
    network_id = await db_access.execute_query("SELECT network.id FROM network WHERE client_id=%s AND name=%s;",
                                               (client_id, network_name))
    return await db_access.execute_query(
        "SELECT device.mac, device.ip, device.vendor FROM device WHERE network_id=%s AND mac=%s;",
        (network_id, mac_address))