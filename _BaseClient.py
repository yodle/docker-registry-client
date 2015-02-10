from requests import get, put, delete
import json


class BaseClient(object):
    """
    Base client class for docker registry
    
    Implements client requests for the Docker Registry API from https://docs.docker.com/reference/api/registry_api

    Attributes:
        host: str -> url of the registry
    """

    IMAGE_LAYER = '/v1/images/{image_id}/layer'
    IMAGE_JSON = '/v1/images/{image_id}/json'
    IMAGE_ANCESTRY = '/v1/images/{image_id}/ancestry'
    REPO = '/v1/repositories/{namespace}/{repository}'
    TAGS = REPO + '/tags'

    def __init__(self, host):
        self.host = host

    def search(self, q=''):
        """
        Request:      GET /v1/search?q=search_term&page=1&n=25 HTTP/1.1

        Response:         HTTP/1.1 200 OK
                          Vary: Accept
                          Content-Type: application/json

                          {"num_pages": 1,
                            "num_results": 3,
                            "results" : [
                               {"name": "ubuntu", "description": "An ubuntu image..."},
                               {"name": "centos", "description": "A centos image..."},
                               {"name": "fedora", "description": "A fedora image..."}
                             ],
                            "page_size": 25,
                            "query":"search_term",
                            "page": 1
                          }
        """
        if q: q = '?q=' + q
        return self._http_call('/v1/search' + q, get)

    def check_status(self):
        """
        Request:      GET /v1/_ping HTTP/1.1

        Response:     HTTP/1.1 200
        """
        return self._http_call('/v1/_ping', get)

    def get_image_layer(self, image_id):
        """
        Request:      GET /v1/images/(image_id)/layer HTTP/1.1
                      Transfer-Encoding: chunked
                      Authorization: Token signature=123abc,repository="foo/bar",access=read

        Response:     HTTP/1.1 200
                      Cookie: (Cookie provided by the Registry)

                      {layer binary data stream}
        """
        return self._http_call(self.IMAGE_LAYER, get, image_id=image_id)

    def put_image_layer(self, image_id, data):
        """
        Request:      PUT /v1/images/(image_id)/layer HTTP/1.1
                      Transfer-Encoding: chunked
                      Authorization: Token signature=123abc,repository="foo/bar",access=write

                      {layer binary data stream}

        Response:     HTTP/1.1 200
        """
        # TODO: Add Transfer-Encoding Header
        # TODO: Get auth token and add it appropriately
        return self._http_call(self.IMAGE_LAYER, put, image_id=image_id, data=data)

    def put_image_metadata(self, image_id, data):
        """
        Request:      PUT /v1/images/(image_id)/json HTTP/1.1
                      Accept: application/json
                      Content-Type: application/json
                      Cookie: (Cookie provided by the Registry)
                      Body:
                      {
                            id: ImageId,
                            parent: ImageId,
                            created: TimeStamp,
                            container: ImageId,
                            container_config: {
                                Hostname: "host-test",
                                User: "",
                                Memory: 0,
                                MemorySwap: 0,
                                AttachStdin: false,
                                AttachStdout: false,
                                AttachStderr: false,
                                PortSpecs: null,
                                Tty: false,
                                OpenStdin: false,
                                StdinOnce: false,
                                Env: null,
                                Cmd: [
                                    "/bin/bash",
                                    "-c",
                                    "apt-get -q -yy -f install libevent-dev"
                                ],
                                Dns: null,
                                Image: "imagename/blah",
                                Volumes: { },
                                VolumesFrom: ""
                            },
                            docker_version: "0.1.7"
                      }

        Response:
                      HTTP/1.1 200
        """
        return self._http_call(self.IMAGE_JSON, put, data=data, image_id=image_id)

    def get_image_metadata(self, image_id):
        """
        Request:      GET /v1/images/(image_id)/json HTTP/1.1

        Response:     HTTP/1.1 200
                      Content-Type: application/json
                      X-Docker-Size: 456789
                      X-Docker-Checksum: b486531f9a779a0c17e3ed29dae8f12c4f9e89cc6f0bc3c38722009fe6857087

                      {
                          id: ImageId,
                          parent: ImageId,
                          created: TimeStamp,
                          container: ImageId,
                          container_config: {
                              Hostname: "host-test",
                              User: "",
                              Memory: 0,
                              MemorySwap: 0,
                              AttachStdin: false,
                              AttachStdout: false,
                              AttachStderr: false,
                              PortSpecs: null,
                              Tty: false,
                              OpenStdin: false,
                              StdinOnce: false,
                              Env: null,
                              Cmd: [
                              "/bin/bash",
                              "-c",
                              "apt-get -q -yy -f install libevent-dev"
                              ],
                              Dns: null,
                              Image: "imagename/blah",
                              Volumes: { },
                              VolumesFrom: ""
                          },
                          docker_version: "0.1.7"
                      }
        """
        return self._http_call(self.IMAGE_JSON, get, image_id=image_id)

    def get_image_ancestry(self, image_id):
        """
        Request:      GET /v1/images/(image_id)/ancestry HTTP/1.1

        Response:
                      HTTP/1.1 200
                      Content-Type: application/json

                     [<ImageIds>]
        """
        return self._http_call(self.IMAGE_ANCESTRY, get, image_id=image_id)

    def get_repository_tags(self, namespace, repository):
        """
        Request:      GET /v1/repositories/(namespace)/(repository)/tags HTTP/1.1

        Response:
                      HTTP/1.1 200
                      Content-Type: application/json

                      {<Tag>: <ImageId>, ...>}
        """
        return self._http_call(self.TAGS, get, namespace=namespace, repository=repository)

    def get_image_id(self, namespace, respository, tag):
        """
        Request:      GET /v1/repositories/(namespace)/(repository)/tags/(tag*) HTTP/1.1

        Response:
                      HTTP/1.1 200

                      <ImageId>
        """
        return self._http_call(self.TAGS + '/' + tag, get,
                               namespace=namespace, repository=respository)

    def delete_repository_tag(self, namespace, repository, tag):
        """
        Request:      DELETE /v1/repositories/(namespace)/(repository)/tags/(tag*) HTTP/1.1
                      Cookie: (Cookie provided by the Registry)

        Response:     HTTP/1.1 200
        """
        # TODO: Get the cookie and add it to the request if it's really required
        return self._http_call(self.TAGS + '/' + tag, delete,
                               namespace=namespace, repository=repository)

    def set_tag(self, namespace, repository, tag, image_id):
        """
        Request:      PUT /v1/repositories/(namespace)/(repository)/tags/(tag*) HTTP/1.1
                      Cookie: (Cookie provided by the Registry)

                      <ImageId>

        Response:
                     HTTP/1.1 200
        """
        return self._http_call(self.TAGS + '/' + tag, put,
                               namespace=namespace, repository=repository, data=image_id)

    def _delete_repository(self, namespace, repository):
        """
        Request:      DELETE /v1/repositories/(namespace)/(repository)/ HTTP/1.1

        Response:
                      HTTP/1.1 200
        """
        return self._http_call(self.REPO, delete, namespace=namespace, repository=repository)

    def _http_call(self, url, method, data="", header=None, auth=None, **kwargs):
        """
        :param url: method prefixed target url with format placeholders -> http://www.example.com/{id}
        :param method: actual method to use for the call -> get, put, delet
        :param data: body of call
        :param header: http header if required
        :param kwargs: args for formatting url
        :return: response json
        """
        if header is None:
            header = {'content-type': 'application/json'}
        return method(self.host + url.format(**kwargs), data=json.dumps(data), headers=header, auth=auth).json()

