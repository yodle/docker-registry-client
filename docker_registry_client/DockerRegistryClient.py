from __future__ import absolute_import

from docker_registry_client._BaseClient import BaseClient
from docker_registry_client.Repository import Repository


class DockerRegistryClient(object):
    def __init__(self, host, verify_ssl=None):
        self._base_client = BaseClient(host, verify_ssl=verify_ssl)
        self._repositories = {}
        self._repositories_by_namespace = {}
        self.refresh()

    def namespaces(self):
        return list(self._repositories_by_namespace.keys())

    def repository(self, repository, namespace=None):
        if '/' in repository:
            if namespace is not None:
                raise RuntimeError('cannot specify namespace twice')
            namespace, repository = repository.split('/', 1)

        return Repository(self._base_client, repository, namespace=namespace)

    def repositories(self, namespace=None):
        if namespace:
            return self._repositories_by_namespace[namespace]

        return self._repositories

    def refresh(self):
        if self._base_client.version == 1:
            self._refresh_v1()
        else:
            assert self._base_client.version == 2
            self._refresh_v2()

    def _refresh_v1(self):
        _repositories = self._base_client.search()['results']
        for repository in _repositories:
            name = repository['name']
            ns, repo = name.split('/', 1)

            r = Repository(self._base_client, repo, namespace=ns)
            self._repositories_by_namespace.setdefault(ns, {})
            self._repositories_by_namespace[ns][name] = r
            self._repositories[name] = r

    def _refresh_v2(self):
        repositories = self._base_client.catalog()['repositories']
        for name in repositories:
            try:
                ns, repo = name.split('/', 1)
            except ValueError:
                ns = None
                repo = name

            r = Repository(self._base_client, repo, namespace=ns)

            if ns is None:
                ns = 'library'

            self._repositories_by_namespace.setdefault(ns, {})
            self._repositories_by_namespace[ns][name] = r
            self._repositories[name] = r
