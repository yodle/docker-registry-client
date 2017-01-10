from __future__ import absolute_import

import time

import requests
from requests import exceptions
import docker
import pytest
from docker import utils as docker_utils


@pytest.fixture(scope='session')
def docker_client():
    client_cfg = docker_utils.kwargs_from_env()
    return docker.Client(version='1.21', **client_cfg)


def wait_till_up(url, attempts):
    for i in range(attempts-1):
        try:
            requests.get(url)
            return
        except exceptions.ConnectionError as e:
            time.sleep(0.1 * 2**i)
    else:
        requests.get(url)


@pytest.yield_fixture()
def registry(docker_client):
    cli = docker_client
    cli.pull('registry', '2')
    cont = cli.create_container(
        'registry:2',
        ports=[5000],
        host_config=cli.create_host_config(
            port_bindings={
                5000: 5000,
            },
        ),
    )
    try:
        cli.start(cont)
        wait_till_up('http://localhost:5000', 3)
        try:
            yield
        finally:
            cli.stop(cont)
    finally:
        cli.remove_container(cont, v=True, force=True)
