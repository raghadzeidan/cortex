import pytest
from cortex.client.client_utils import Reader, UNCOMPRESSED
from cortex.client import FILE_FORMAT

@pytest.fixture
def read_path(tmp_path):
	f = tmp_path / 'file.txt'
	return str(f)

def test_f(read_path):
	with open(read_path, "w") as f:
		f.write('Raghd')
	path_suit = f'{FILE_FORMAT}{read_path}/?compressor={UNCOMPRESSED}'
	reader = Reader(path_suit)
	assert 1==2
