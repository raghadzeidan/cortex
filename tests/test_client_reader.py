import pytest
import gzip
import requests
from cortex.server import run_server
from cortex.client import FILE_FORMAT, upload_sample


MOCK_SAMPLE = b'\x08*\x12\nDan Gittik\x18\xe0\x90\xd5\xcd\x02'
@pytest.fixture
def read_path(tmp_path):
	f = tmp_path / 'file.gz'
	return str(f)



def test_my_client(httpserver): 
    httpserver.expect_request("/foobar").respond_with_json({"foo": "bar"})
    run_server(host='127.0.0.1', port=8000, publish=print)
    assert requests.get(httpserver.url_for("/foobar")).json() == {'foo': 'bar'}


