from mock import patch
import _BaseClient

host = "http://docker-registry.example.com"
client = _BaseClient.BaseClient(host)

@patch('_BaseClient.get')
def test_search_uses_correct_parameters(get):
    client.search(q="abc=123,def=ghi")

    get.assert_called_once_with(host + '/v1/search?q=abc=123,def=ghi', data='""',
                                headers={'content-type': 'application/json'}, auth=None)

@patch('_BaseClient.get')
def test_check_status_calls_correct_url(get):
    client.check_status()
    get.assert_called_once_with(host + '/v1/_ping', data='""',
                                headers={'content-type': 'application/json'}, auth=None)

@patch('_BaseClient.get')
def test_get_image_layer_calls_correct_url(get):
    image_id = '12345'
    client.get_image_layer(image_id)
    get.assert_called_once_with(host + '/v1/images/12345/layer', data='""',
                                headers={'content-type': 'application/json'}, auth=None)

@patch('_BaseClient.put')
def test_put_image_layer_calls_correct_url_with_body(put):
    # TODO: This should verify the transfer encoding, and probably not use content-type. Also requires authorization
    image_id = '12345'
    image_data = '0x0123456789ABCDEF'  # Just some binary data
    client.put_image_layer(image_id, image_data)
    put.assert_called_once_with(host + '/v1/images/12345/layer', data='"' + image_data + '"',
                                headers={'content-type': 'application/json'}, auth=None)

@patch('_BaseClient.get')
def test_put_image_metadata_calls_correct_url(get):
    image_id = '12345'
    client.get_image_metadata(image_id)
    get.assert_called_once_with(host + '/v1/images/12345/json', data='""',
                                headers={'content-type': 'application/json'}, auth=None)