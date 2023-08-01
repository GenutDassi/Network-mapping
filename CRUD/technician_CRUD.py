from DB import db_access
from authorization_and_authentication import authorization_and_authentication


async def add_technician(technician_name, technician_password):
    query = """INSERT IGNORE INTO technician (name, password) VALUES (%s, %s)"""
    return await db_access.execute_query(query, (technician_name, technician_password))


async def is_authorized(technician_id, client_id):
    query = f'SELECT id FROM permission WHERE client_id = %s AND technician_id = %s'
    authorized = await db_access.execute_query(query, (client_id, technician_id))
    if authorized:
        return True
    return False


async def get_current_technician():
    current_technician_name = await authorization_and_authentication.get_current_technician_name()
    query = f'SELECT technician.id FROM technician WHERE technician.name = %s'
    technician_id = await db_access.execute_query(query, current_technician_name)
    return technician_id
