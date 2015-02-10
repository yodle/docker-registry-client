from mock import patch
import DockerRegistryClient
from Repository import Repository


@patch('DockerRegistryClient.BaseClient')
def test_namespaces_returns_all(baseClient):
    search = lambda: {
        "num_results": 'Does not matter',
        "query": "Does not matter either",
        "results": [{"description": "a container", "name": "lib/container1"},
                    {"description": "another container", "name": "lib/container2"},]
    }

    get_repository_tags = lambda a, b: {'1.1': '123abc', '1.2': '456def'}

    fake = lambda: None
    fake.search = search
    fake.get_repository_tags = get_repository_tags
    baseClient.return_value = fake

    client = DockerRegistryClient.DockerRegistryClient("http://www.example.com")
    ns = client.namespaces()
    assert len(ns) == 1, len(ns)
    assert ns[0] == 'lib'


@patch('DockerRegistryClient.BaseClient')
def test_repositories_returns_list_of_repositories(baseClient):
    search = lambda: {
        "num_results": 'Does not matter',
        "query": "Does not matter either",
        "results": [{"description": "a container", "name": "lib/container1"},
                    {"description": "another container", "name": "lib/container2"},]
    }

    get_repository_tags = lambda a, b: {'1.1': '123abc', '1.2': '456def'}

    fake = lambda: None
    fake.search = search
    fake.get_repository_tags = get_repository_tags
    baseClient.return_value = fake

    client = DockerRegistryClient.DockerRegistryClient("http://www.example.com")
    repos = client.repositories('lib')
    assert len(repos) == 2
    for repo in repos:
        assert isinstance(repo, Repository)