import tempfile
import os
import os.path
import shutil
from flask import Flask, current_app

from config import Config

from utils import write_file_to_fd_while_calculating_md5, create_md5_sum_for_file
from converter import convert_caff_to_tga, convert_tga_to_png

app = Flask(__name__)
app.config.from_object(Config)


def do_everything(workdir: str):
    # Recieve file
    uploaded_caff_fd, uploaded_caff_path = tempfile.mkstemp(suffix='.caff', dir=workdir)

    uploaded_caff_md5sum = write_file_to_fd_while_calculating_md5(uploaded_caff_fd)  # Throws overflow error

    # Convert CAFF to TGA
    converted_tga_fd, converted_tga_path = tempfile.mkstemp(suffix='.tga', dir=workdir)
    os.close(converted_tga_fd)

    convert_caff_to_tga(uploaded_caff_path, converted_tga_path)

    if not os.path.isfile(converted_tga_path):
        raise FileNotFoundError("Conversion output is missing")

    # Convert TGA to PNG
    converted_png_fd, converted_png_path = tempfile.mkstemp(suffix='.png', dir=workdir)
    os.close(converted_png_fd)

    convert_tga_to_png(converted_tga_path, converted_png_path)

    if not os.path.isfile(converted_tga_path):
        raise FileNotFoundError("Conversion output is missing")

    converted_png_md5sum = create_md5_sum_for_file(converted_png_path)

    # Send back converted file
    converted_png_handle = open(converted_png_path, 'rb')

    def stream_and_remove_file():
        # This really is some black magic here
        # When flask transmits the file ...
        yield from converted_png_handle  # <- It transmits from file handle
        # After it's done the rest of this function will be called, so it cleans up after itself
        converted_png_handle.close()
        shutil.rmtree(workdir)

    return current_app.response_class(
        stream_and_remove_file(),
        headers={
            'X-request-checksum': uploaded_caff_md5sum,
            'X-response-checksum': converted_png_md5sum,
            'Content-type': 'image/png'
        }
    )


@app.route('/preview', methods=['POST'])
def perform_conversion():
    workdir = tempfile.mkdtemp(prefix='caff')
    try:
        response = do_everything(workdir)  # normally this would clean up workdir
    except:
        shutil.rmtree(workdir)  # but sometimes it must be done externally
        raise

    return response


if __name__ == '__main__':
    app.run(debug=True)  # nosec: app only launches in debug mode... if it's launched in developement mode
