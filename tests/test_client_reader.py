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



def test_my_client(read_ath): 
    assert 1==1


