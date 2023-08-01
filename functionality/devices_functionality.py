from CRUD import technician_CRUD, device_CRUD
from authorization_and_authentication import authorization_and_authentication


async def get_devices(client_id, network_name):
    technician_id = await technician_CRUD.get_current_technician()
    # technician_id = authorization_and_authentication.get_current_technician()
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return await device_CRUD.get_devices(client_id, network_name)


async def get_devices_by_vendor(client_id, network_name, vendor_name):
    technician_id = await technician_CRUD.get_current_technician()
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return await device_CRUD.get_devices_by_vendor(client_id, network_name, vendor_name)


async def get_devices_by_mac_address(client_id, network_name, mac_address):
    technician_id = await technician_in_db.get_current_technician()
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return await devices_in_db.get_devices_by_mac_address(client_id, network_name, mac_address)