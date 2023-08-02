from CRUD import technician_CRUD, device_CRUD
from authorization_and_authentication import authorization_and_authentication
from exception_decorators.catch_exception import catch_exception


@catch_exception
async def get_devices(client_id, network_name):
    technician_id = await technician_CRUD.get_current_technician()
    # technician_id = authorization_and_authentication.get_current_technician()
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return await device_CRUD.get_devices(client_id, network_name)


@catch_exception
async def get_devices_by_vendor(client_id, network_name, vendor_name):
    technician_id = await technician_CRUD.get_current_technician_id()
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return await device_CRUD.get_devices_by_vendor(client_id, network_name, vendor_name)


@catch_exception
async def get_devices_by_mac_address(client_id, network_name, mac_address):
    technician_id = await technician_CRUD.get_current_technician_id()
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return await device_CRUD.get_devices_by_mac_address(client_id, network_name, mac_address)