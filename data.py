error_page_data = {
    'title': 'Page not found',
    'error_message': 'Page \'{url}\' could not be found'
}

index_data = {
    'title': 'why\'',
    'name': 'Egor Nosov',
    'position': 'Python Developer',
    'image': '/images/avatar.jpg'
}

# hidden service related data

key_path = '.hidden_service_key/keyV3'

host = '127.0.0.1'
control_port = 9051
local_port = 5000
service_port = 80
workers_count = 4

hidden_service_ports_mapping = {
    service_port: local_port
}

hidden_service_server_data = {
    'host': host,
    'port': local_port,
    'workers': workers_count
}

tor_config_data = {
    'ControlPort': str(control_port)
}
