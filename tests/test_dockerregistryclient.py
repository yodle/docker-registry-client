from __future__ import absolute_import

from docker_registry_client import DockerRegistryClient

from flexmock import flexmock
from docker_registry_client import _BaseClient


class TestDockerRegistryClient(object):
    def test_init(self):
        class Response(object):
            def __init__(self):
                self.ok = True

            def raise_for_status(self):
                pass

            def json(self):
                return {'results': {}}

        (flexmock(_BaseClient)
            .should_receive('get')
            .and_return(Response()))
        client = DockerRegistryClient('https://host:5000')
