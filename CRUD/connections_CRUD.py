from DB import db_access
from exception_decorators.catch_exception import catch_exception


@catch_exception
async def add_protocol_to_connection(connection_id, protocol):
    previous_protocols = await db_access.execute_query("SELECT protocol FROM connection WHERE id=%s", connection_id)
    previous_protocols = previous_protocols[0]["protocol"]
    uptodate_protocols = f"{previous_protocols}, {protocol}"
    await db_access.execute_query("UPDATE connection SET protocol = %s WHERE id = %s;",
                                  (uptodate_protocols, connection_id))


@catch_exception
async def create_connection(src_id, dst_id, protocol):
    await db_access.execute_query(
        "INSERT IGNORE INTO connection (src_device_id, dst_device_id, protocol) VALUES (%s, %s, %s);",
        (src_id, dst_id, protocol))
    new_connection_id = await db_access.execute_query("SELECT LAST_INSERT_ID()")
    new_connection_id = new_connection_id[0]["LAST_INSERT_ID()"]
    return new_connection_id
