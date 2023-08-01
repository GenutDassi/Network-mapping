from fastapi import APIRouter, Form, UploadFile, File, Depends

from authorization_and_authentication.authorization_and_authentication import get_current_active_technician
from authorization_and_authentication.authorization_and_authentication_patterns import Technician
from functionality import network_functionality, connection_functionality, devices_functionality


router = APIRouter()


@router.get("/")
async def root():
    print("server is running!!!")
    return {"message": "hello"}


@router.get("/network/information/{client_id}/{network_name}")
async def get_network_information(client_id: int, network_name: str, current_technician: Technician = Depends(get_current_active_technician)):
    return await network_functionality.get_network_information(current_technician, client_id, network_name)


@router.get("/network/connections/{client_id}/{network_name}")
async def get_network_connections(client_id: int, network_name: str, current_technician: Technician = Depends(get_current_active_technician)):
    return await connection_functionality.get_connections(client_id, network_name, current_technician.id)


@router.get("/network/devices-by-vendor/{client_id}/{network_name}/{mapping_by}/{value_mapping}")
async def get_network_devices_by_mapping(client_id: int, network_name: str, mapping_by: str, value_mapping: str, current_technician: Technician = Depends(get_current_active_technician)):
    if mapping_by == "vendor":
        return await devices_functionality.get_devices_by_vendor(current_technician.id, client_id, network_name, value_mapping)
    elif mapping_by == "mac_address":
        return await devices_functionality.get_devices_by_mac_address(current_technician.id, client_id, network_name, value_mapping)


@router.get("/network/devices/{client_id}/{network_name}")
async def get_network_devices(client_id: int, network_name: str, current_technician: Technician = Depends(get_current_active_technician)):
    return await devices_functionality.get_devices(current_technician.id, client_id, network_name)


@router.post("/network/add_network")
async def add_network(client_id: int, network_name: str = Form(...), network_location: str = Form(...),  file: UploadFile = File(...), current_technician: Technician = Depends(get_current_active_technician)):
    file_content = await file.read()
    return await network_functionality.add_network(current_technician, client_id, network_name, network_location, file_content)


