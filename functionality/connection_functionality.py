from CRUD import technician_CRUD, network_CRUD
from authorization_and_authentication import authorization_and_authentication
from exception_decorators.catch_exception import catch_exception


@catch_exception
async def get_connections(client_id, network_name):
    technician_id = await technician_CRUD.get_current_technician_id()
    # technician_id = authorization_and_authentication.get_current_technician()
    if authorization_and_authentication.check_permission(technician_id, client_id):
        return await network_CRUD.get_full_network(client_id, network_name)
