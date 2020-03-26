def read_bytes(fd, data_size, return_as=None):
    data = fd.read(data_size)
    if return_as:
        return render_from_bytes(data) if return_as==int else data.decode('utf-8')
    return data


