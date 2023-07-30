import db_access


async def add_technician(technician_name, technician_password):
    query = """INSERT IGNORE INTO technician (name, password) VALUES (%s, %s)"""
    return await db_access.execute_query(query, (technician_name, technician_password))


async def is_authorized(technician_id, client_id):
    query = f'SELECT id FROM permission WHERE client_id = {client_id} AND technician_id = {technician_id}'
    authorized = await db_access.execute_query(query)
    if authorized:
        return True
    return False

