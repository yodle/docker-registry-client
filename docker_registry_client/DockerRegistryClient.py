from _BaseClient import BaseClient
from Repository import Repository


class DockerRegistryClient(object):
    def __init__(self, host):
        self._base_client = BaseClient(host)
        self._repositories = {}
        self.refresh()

    def namespaces(self):
        return self._repositories.keys()

    def repositories(self, namespace):
        return self._repositories[namespace]

    def refresh(self):
        _repositories = self._base_client.search()['results']
        for repository in _repositories:
            name = repository['name']
            ns, repo = name.split('/')
            r = Repository(self._base_client, ns, repo)
            if ns in self._repositories:
                self._repositories[ns].append(r)
            else:
                self._repositories[ns] = [r]
