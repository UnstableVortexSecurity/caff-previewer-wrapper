from flask import request, current_app
import werkzeug.exceptions
import hashlib


def write_file_to_fd_while_calculating_md5(fd: int) -> str:
    chunksize = current_app.config['RECIEVE_CHUNKSIZE']
    m = hashlib.md5()  # nosec: md5 is used only for integrity checking here

    total_recieved = 0

    # Begin recieving the file
    with open(fd, "bw") as f:

        while True:  # This is where uploading happens
            chunk = request.stream.read(chunksize)
            if len(chunk) == 0:
                break

            total_recieved += len(chunk)
            if total_recieved > current_app.config['MAX_RECIEVE_SIZE']:
                raise werkzeug.exceptions.RequestEntityTooLarge()

            m.update(chunk)
            f.write(chunk)

    return m.hexdigest()


def create_md5_sum_for_file(fname):
    m = hashlib.md5()  # nosec: md5 is used only for integrity checking here

    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            m.update(chunk)

    return m.hexdigest()
