"""
Copyright 2015 Red Hat, Inc

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


from __future__ import absolute_import

import argparse
from docker_registry_client import DockerRegistryClient
import logging
import requests


class CLI(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        excl_group = self.parser.add_mutually_exclusive_group()
        excl_group.add_argument("-q", "--quiet", action="store_true")
        excl_group.add_argument("-v", "--verbose", action="store_true")

        self.parser.add_argument('--verify-ssl', dest='verify_ssl',
                                 action='store_true')
        self.parser.add_argument('--no-verify-ssl', dest='verify_ssl',
                                 action='store_false')

        self.parser.add_argument('registry', metavar='REGISTRY', nargs=1,
                                 help='registry URL (including scheme)')
        self.parser.add_argument('repository', metavar='REPOSITORY', nargs='?')

        self.parser.set_defaults(verify_ssl=True)

    def run(self):
        args = self.parser.parse_args()

        basic_config_args = {}
        if args.verbose:
            basic_config_args['level'] = logging.DEBUG
        elif args.quiet:
            basic_config_args['level'] = logging.WARNING

        logging.basicConfig(**basic_config_args)

        client = DockerRegistryClient(args.registry[0],
                                      verify_ssl=args.verify_ssl)

        if args.repository:
            self.show_tags(client, args.repository)
        else:
            self.show_repositories(client)

    def show_repositories(self, client):
        try:
            repositories = client.repositories()
        except requests.HTTPError as e:
            if e.response.status_code == requests.codes.not_found:
                print("Catalog/Search not supported")
            else:
                raise
        else:
            print("Repositories:")
            for repository in repositories.keys():
                print("  - {0}".format(repository))

    def show_tags(self, client, repository):
        try:
            repo = client.repository(repository)
        except requests.HTTPError as e:
            if e.response.status_code == requests.codes.not_found:
                print("Repository {0} not found".format(repository))
            else:
                raise
        else:
            print("Tags in repository {0}:".format(repository))
            for tag in repo.tags():
                print("  - {0}".format(tag))


if __name__ == '__main__':
    try:
        cli = CLI()
        cli.run()
    except KeyboardInterrupt:
        pass
