def read_bytes(fd, data_size, return_as=None):
    data = fd.read(data_size)
    if return_as:
        return render_from_bytes(data) if return_as==int else data.decode('utf-8')
    return data


def render_from_bytes(byytes):
    result = 0
    for b in byytes:
        result = result * 256 + int(b)
    return result
def render_to_bytes(string, num_bytes):
	barray = bytearray(string.to_bytes(num_bytes, sys.byteorder))
	bbytes = bytes(barray)
	return bbytes
