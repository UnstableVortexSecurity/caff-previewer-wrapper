import os


class Config:
    CAFF_PREVIEWER_BINARY = os.environ.get('CAFF_PREVIEWER_BINARY', '/usr/local/bin/caff_previewer')
    IMAGEMAGICK_CONVERT_BINARY = os.environ.get('IMAGEMAGICK_CONVERT_BINARY', '/usr/bin/convert')
    CONVERSION_TIMEOUT = int(os.environ.get('CONVERSION_TIMEOUT', 30))
    RECIEVE_CHUNKSIZE = int(os.environ.get('RECIEVE_CHUNKSIZE', 4096))
    MAX_RECIEVE_SIZE = int(os.environ.get('MAX_RECIEVE_SIZE', 536870912))  # 512 MB
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    RELEASE_ID = os.environ.get('RELEASE_ID', 'test')
    RELEASEMODE = os.environ.get('RELEASEMODE', 'dev')
