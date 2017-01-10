from docker_registry_client import BaseClient


def test_base_client(registry):
    cli = BaseClient('http://localhost:5000', api_version=2)
    assert cli.catalog() == {'repositories': []}
