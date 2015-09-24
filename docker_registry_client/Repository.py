from __future__ import absolute_import

from docker_registry_client.Image import Image


class RepositoryV1(object):
    def __init__(self, client, namespace, name):
        self._client = client
        self.namespace = namespace
        self.name = name
        self._images = None
        self.refresh()

    def __repr__(self):
        return 'RepositoryV1({ns}/{name})'.format(ns=self.namespace,
                                                  name=self.name)

    def refresh(self):
        self._images = self._client.get_repository_tags(self.namespace,
                                                        self.name)

    def tags(self):
        return list(self._images.keys())

    def data(self, tag):
        return self._client.get_tag_json(self.namespace, self.name, tag)

    def image(self, tag):
        image_id = self._images[tag]
        return Image(image_id, self._client)

    def untag(self, tag):
        return self._client.delete_repository_tag(self.namespace,
                                                  self.name, tag)

    def tag(self, tag, image_id):
        return self._client.set_tag(self.namespace,
                                    self.name, tag, image_id)

    def delete_repository(self):
        # self._client.delete_repository(self.namespace, self.name)
        raise NotImplementedError()


def Repository(client, namespace, name):
    assert client.version == 1
    return RepositoryV1(client, namespace, name)
