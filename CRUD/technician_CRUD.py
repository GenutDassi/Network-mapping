from DB import db_access


async def add_technician(technician_name, technician_password):
    query = """INSERT IGNORE INTO technician (name, password) VALUES (%s, %s)"""
    return await db_access.execute_query(query, (technician_name, technician_password))

