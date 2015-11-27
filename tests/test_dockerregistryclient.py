from __future__ import absolute_import

from docker_registry_client import DockerRegistryClient
import pytest
from tests.mock_registry import (mock_registry,
                                 mock_v2_registry,
                                 TEST_NAMESPACE,
                                 TEST_REPO,
                                 TEST_NAME,
                                 TEST_TAG)


class TestDockerRegistryClient(object):
    @pytest.mark.parametrize('version', [1, 2])
    def test_namespaces(self, version):
        url = mock_registry(version)
        client = DockerRegistryClient(url)
        assert client.namespaces() == [TEST_NAMESPACE]

    @pytest.mark.parametrize('version', [1, 2])
    @pytest.mark.parametrize(('repository', 'namespace'), [
        (TEST_REPO, None),
        (TEST_REPO, TEST_NAMESPACE),
        ('{0}/{1}'.format(TEST_NAMESPACE, TEST_REPO), None),
    ])
    def test_repository(self, version, repository, namespace):
        url = mock_registry(version)
        client = DockerRegistryClient(url)
        repository = client.repository(repository, namespace=namespace)
        assert isinstance(repository, MockRegistry)

    @pytest.mark.parametrize('version', [1, 2])
    def test_repository(self, version):
        url = mock_registry(version)
        client = DockerRegistryClient(url)
        with pytest.raises(RuntimeError):
            client.repository('{0}/{1}'.format(TEST_NAMESPACE, TEST_REPO),
                              namespace=TEST_NAMESPACE)

    @pytest.mark.parametrize('namespace', [TEST_NAMESPACE, None])
    @pytest.mark.parametrize('version', [1, 2])
    def test_repositories(self, version, namespace):
        url = mock_registry(version)
        client = DockerRegistryClient(url)
        repositories = client.repositories(TEST_NAMESPACE)
        assert len(repositories) == 1
        assert TEST_NAME in repositories
        repository = repositories[TEST_NAME]
        assert repository.name == "%s/%s" % (TEST_NAMESPACE, TEST_REPO)

    @pytest.mark.parametrize('version', [1, 2])
    def test_repository_tags(self, version):
        url = mock_registry(version)
        client = DockerRegistryClient(url)
        repositories = client.repositories(TEST_NAMESPACE)
        assert TEST_NAME in repositories
        repository = repositories[TEST_NAME]
        tags = repository.tags()
        assert len(tags) == 1
        assert TEST_TAG in tags

    def test_repository_manifest(self):
        url = mock_v2_registry()
        client = DockerRegistryClient(url)
        repository = client.repositories()[TEST_NAME]
        manifest, digest = repository.manifest(TEST_TAG)
        repository.delete_manifest(digest)
