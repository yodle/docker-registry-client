# code extracted from https://git.io/vM0EB used under license:
#
# Copyright (c) 2015 David Halls <https://github.com/davedoesdev/>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import base64
import ecdsa
import jws
import json


def assign(obj, *objs):
    for o in objs:
        obj.update(o)
    return obj


def force_bytes(s, encoding='utf8'):
    return s if isinstance(s, bytes) else s.encode(encoding)


def _urlsafe_b64encode_bytes(b):
    return base64.urlsafe_b64encode(b).rstrip(b'=').decode('utf-8')


def _urlsafe_b64encode(s):
    return _urlsafe_b64encode_bytes(force_bytes(s))


jws.utils.to_bytes_2and3 = force_bytes
jws.algos.to_bytes_2and3 = force_bytes


def _num_to_base64(n):
    b = bytearray()
    while n:
        b.insert(0, n & 0xFF)
        n >>= 8
    # need to pad to 32 bytes
    while len(b) < 32:
        b.insert(0, 0)
    return _urlsafe_b64encode_bytes(b)


def sign(manifest, key=None):
    m = assign({}, manifest)

    try:
        del m['signatures']
    except KeyError:
        pass

    assert len(m) > 0

    manifest_json = json.dumps(m, sort_keys=True)

    if key is None:
        key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)

    manifest64 = _urlsafe_b64encode(manifest_json)
    format_length = manifest_json.rfind('}')
    format_tail = manifest_json[format_length:]
    protected_json = json.dumps({
        'formatLength': format_length,
        'formatTail': _urlsafe_b64encode(format_tail)
    })
    protected64 = _urlsafe_b64encode(protected_json)
    point = key.privkey.public_key.point
    data = {
        'key': key,
        'header': {
            'alg': 'ES256'
        }
    }
    jws.header.process(data, 'sign')
    sig = data['signer']("%s.%s" % (protected64, manifest64), key)
    signatures = [{
        'header': {
            'jwk': {
                'kty': 'EC',
                'crv': 'P-256',
                'x': _num_to_base64(point.x()),
                'y': _num_to_base64(point.y())
            },
            'alg': 'ES256'
        },
        'signature': _urlsafe_b64encode(sig),
        'protected': protected64
    }]
    return (
        manifest_json[:format_length] +
        ', "signatures": ' +
        json.dumps(signatures) +
        format_tail
    )
