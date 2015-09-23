from __future__ import absolute_import

from docker_registry_client.Repository import Repository
from docker_registry_client._BaseClient import BaseClient

from flexmock import flexmock
from docker_registry_client import _BaseClient


class TestRepository(object):
    def test_init(self):
        class Response(object):
            def __init__(self):
                self.ok = True

            def raise_for_status(self):
                pass

            def json(self):
                return {}

        (flexmock(_BaseClient)
            .should_receive('get')
            .and_return(Response())
            .once())
        client = BaseClient('https://host:5000')
        repo = Repository(client, 'namespace', 'repo')
