import pytest
import gzip
import requests
from cortex.client.client_utils import Reader, UNCOMPRESSED
from cortex.client import FILE_FORMAT, upload_sample


MOCK_SAMPLE = b'\x08*\x12\nDan Gittik\x18\xe0\x90\xd5\xcd\x02'
@pytest.fixture
def read_path(tmp_path):
	f = tmp_path / 'file.gz'
	return str(f)

#def test_f(read_path):
#	print(read_path)
#	y = ''
#	with open(read_path, "wb") as f:
#		f.write(USER_BYTES)
#	print(y)
#	path_suit = f'{FILE_FORMAT}{read_path}/?compressor=gzip'
#	reader = Reader(path_suit)
#	x = reader.user
#	print(x)
#	assert 1==2


def test_my_client(httpserver): 
    httpserver.expect_request("/foobar").respond_with_json({"foo": "bar"})
    assert requests.get(httpserver.url_for("/foobar")).json() == {'foo': 'bar'}
