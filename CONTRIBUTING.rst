## Code Style

Follow pep8 and check style with pyflakes

## Testing

Tests are run with `py.test tests`. Please write tests for new code.

## CI

We use travis for CI. The build must be passing in order to merge a pull request.

## Deploying

docker-registry-client is deployed to [pypi](https://pypi.python.org/pypi/docker-registry-client/)

Use zest.releaser to publish new releases

    mkdir ~/.virtualenvs/
    python3 -m venv ~/.virtualenvs/releaser
    source ~/.virtualenvs/releaser/bin/activate
    pip install -U pip setuptools wheel
    pip install zest.releaser
    fullrelease
