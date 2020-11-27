# CAFF Previewer Wrapper
This is a simple wrapper written in Python/Flask that places a very simple HTTP interface in front of the CAFF Previewer with PNG conversion capabilites provided by ImageMagick.

## Endpoint
CAFF Previewer Wrapper exposes a single endpoint only: 

**POST** `/preview`

This endpoint expects a single CAFF file to be posted, and in response it returns a single png file. The raw CAFF file contents is expected in `application/octet-stream` style without any extra encapsulation.

Possible response codes:
 - **200**: Conversion went fine. The response body should be `image/png` and the integrity headers are set. 
 - **400**: CAFF Format violation
 - **413**: Request body length is larger than the configured maximum.
 - **500**: Something went terribly wrong during the creation of the preview. You should check server logs.

## Configure
CAFF Previewer Wrapper can be configured using environmental variables. Currently the following set of envvars are supported:
 - CAFF_PREVIEWER_BINARY: The location of the `caff_previewer` binary (default: /usr/local/bin/caff_previewer)
 - IMAGEMAGICK_CONVERT_BINARY: The location of ImageMagick's convert binary (default: /usr/bin/convert)
 - CONVERSION_TIMEOUT: Timeout for running each converter binary in seconds (If they do not finish in this timeframe they will be killed and an internal server error will be reported) (default: 30)
 - RECIEVE_CHUNKSIZE: Chunk size for writing file to disk and calculating md5 sum. There is really no point tuning this value in most cases. (default: 4096)
 - MAX_RECIEVE_SIZE: Maximum body length to be accepted in bytes. Exceeding results in 413 error. Check is based on the actual size recieved, the `Content-length` header is currently ignored (default: 536870912 = 512 MB)
 - SENTRY_DSN: Sentry DSN. Not setting it disables sentry integration (default not set)
 - RELEASE_ID: Sentry release (default: test)
 - RELEASEMODE: Sentry environment (default: dev)


## Integrity checking
CAFF Previewer Wrapper provides two headers in the response that can be used to check the integrity of transfered files:  
`X-request-checksum` and `X-response-checksum`. The former provides an md5 checksum of the recieved file. The later is the md5 checksum of the converted file.

## Building docker image
In order for this image to be built with the `caff_previewer` binary included, it extracts the binary of the prebuilt `caff_previewer` image. ImageMagick is installed during build time.

## ImageMagick and upside-down images
For some reason different versions/builds of ImageMagick does not properly recognize the origin point of the TGA file saved by `caff_previewer` (See.: http://www.imagemagick.org/discourse-server/viewtopic.php?t=34757). 
To work around this issue the argument `-auto-orient` altrough in some versions this might cause the image to appear upside-down instead, it works with the image-magick version bundled in the docker image.
