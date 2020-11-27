import os.path
import subprocess  # nosec: That's the whole point of this application
from flask import current_app
import werkzeug.exceptions


def run_abstract_converter(converter: str, source: str, destination: str, extra_args: list = None) -> int:
    """
    Just runs a binary and gives it two arguments
    :param converter: the converter binary to run
    :param source: source file
    :param destination: destination file
    :returns: exitcode of the converter
    """
    if not (os.path.isfile(source) and os.path.isfile(converter)):
        raise FileNotFoundError("Source or converter binary does not exists")

    if not extra_args:
        extra_args = []

    completed_process = subprocess.run([converter, *extra_args, source, destination],  # nosec: Concerning arguments checked above
                                       timeout=current_app.config['CONVERSION_TIMEOUT'], env={})

    return completed_process.returncode


def convert_caff_to_tga(source: str, destination: str):
    """
    This function uses caff_previewer to convert a CAFF file into a TGA file
    :param source: path of the source TGA file (must exists)
    :param destination: path of the destination TGA file (will be created)
    """
    INTERNAL_ERROR_CODES = [0x01, 0x03, 0x04, 0x05, 0x32, 0x51]
    ret = run_abstract_converter(current_app.config['CAFF_PREVIEWER_BINARY'], source, destination)
    if ret in INTERNAL_ERROR_CODES:
        raise RuntimeError(f"Caff Previewer returned an unexpected error code: {ret}")
    elif ret != 0:
        raise werkzeug.exceptions.BadRequest("CAFF format violation")


def convert_tga_to_png(source: str, destination: str):
    """
    This function uses ImageMagick to convert a TGA file into a PNG file
    :param source: path of the source TGA file (must exists)
    :param destination: path of the destination TGA file (will be created)
    """
    ret = run_abstract_converter(current_app.config['IMAGEMAGICK_CONVERT_BINARY'], source, destination, ['-auto-orient'])
    if ret != 0:
        raise RuntimeError(f"Image magick convert returned an unexpected error code: {ret}")
