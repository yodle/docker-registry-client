from __future__ import absolute_import

from docker_registry_client.Image import Image
from docker_registry_client._BaseClient import BaseClient


class TestImage(object):
    def test_init(self):
        Image('test_image_id', BaseClient('https://host:5000'))
