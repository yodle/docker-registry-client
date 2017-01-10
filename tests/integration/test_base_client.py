from docker_registry_client import BaseClient
import pkg_resources


def test_base_client(registry):
    cli = BaseClient('http://localhost:5000', api_version=2)
    assert cli.catalog() == {'repositories': []}


def test_base_client_edit_manifest(docker_client, registry):
    cli = BaseClient('http://localhost:5000', api_version=2)
    build = docker_client.build(
        pkg_resources.resource_filename(__name__, 'fixtures/base'),
        'localhost:5000/x-drc-example:x-drc-test', stream=True,
    )
    for line in build:
        print(line)

    push = docker_client.push(
        'localhost:5000/x-drc-example', 'x-drc-test', stream=True,
        insecure_registry=True,
    )

    for line in push:
        print(line)

    m = cli.get_manifest('x-drc-example', 'x-drc-test')
    assert m._content['name'] == 'x-drc-example'
    assert m._content['tag'] == 'x-drc-test'

    cli.put_manifest('x-drc-example', 'x-drc-test-put', m)

    pull = docker_client.pull(
        'localhost:5000/x-drc-example', 'x-drc-test-put', stream=True,
        insecure_registry=True, decode=True,
    )

    pull = list(pull)
    tag = 'localhost:5000/x-drc-example:x-drc-test-put'

    expected_statuses = {
        'Status: Downloaded newer image for ' + tag,
        'Status: Image is up to date for ' + tag,
    }

    errors = [evt for evt in pull if 'error' in evt]
    assert errors == []

    assert {evt.get('status') for evt in pull} & expected_statuses
