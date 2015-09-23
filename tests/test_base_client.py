from __future__ import absolute_import

from docker_registry_client._BaseClient import BaseClient

from flexmock import flexmock
from docker_registry_client import _BaseClient


class TestBaseClient(object):
    def test_check_status(self):
        class Response(object):
            def __init__(self):
                self.ok = True

            def json(self):
                return {}

        (flexmock(_BaseClient)
            .should_receive('get')
            .and_return(Response())
            .once())
        BaseClient('https://host:5000').check_status()
