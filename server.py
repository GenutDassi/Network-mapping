import network_in_db
import pcap_files_access
import authorization_and_authentication


async def login(name, password):
    return authorization_and_authentication.login(name, password)


async def signup(name, password):
    return authorization_and_authentication.signup(name, password)


async def upload_file(client_id, path):
    if authorization_and_authentication.check_permission(client_id):
        return pcap_files_access.upload_file(path)


async def network_information(client_id, network_name):
    if authorization_and_authentication.check_permission(client_id):
        return network_in_db.get_network_info(client_id, network_name)
