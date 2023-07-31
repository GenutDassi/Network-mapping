from pydantic import BaseModel


class NetworkInfo(BaseModel):
    network_name: str
    location: str
    client_name: str


class Device(BaseModel):
    mac: str
    ip: str
    vendor: str


class Connection(BaseModel):
    protocol: str
    src_device: Device
    dst_device: Device


class Network(BaseModel):
    info: NetworkInfo
    connections: list[Connection]
