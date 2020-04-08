from stem.control import Controller
from stem.process import launch_tor_with_config

import logging
import uvicorn

from app import build_application
from data import (
    control_port,
    key_path,
    hidden_service_ports_mapping,
    hidden_service_server_data,
    tor_config_data
)


app = build_application()
logging.basicConfig(level=logging.INFO)


def start_tor_process(config):
    tor_process = launch_tor_with_config(config=config)

    return tor_process


def run_hidden_service(port, key_path):
    tor_process = start_tor_process(config=tor_config_data)

    with Controller.from_port(port=port) as controller:
        controller.authenticate()

        with open(key_path) as key_file:
            key_type, key_content = key_file.read().split(':', 1)

        service = controller.create_ephemeral_hidden_service(ports=hidden_service_ports_mapping,
                                                             key_type=key_type,
                                                             key_content=key_content,
                                                             await_publication=True)
        logging.info(f'Running {service.service_id}.onion')

        try:
            uvicorn.run('hidden_service:app', **hidden_service_server_data)
        finally:
            logging.info('Shutting down our hidden service')
            controller.remove_ephemeral_hidden_service(service.service_id)
            tor_process.terminate()


if __name__ == '__main__':
    run_hidden_service(port=control_port, key_path=key_path)
