FROM dxflrs/garage:v2.3.0 AS base

# The base image is using a scratch image, so we need to copy
# the garage binary in a alpine image, to be able to use a shell
# entrypoint to bootstrap the garage configuration and start
# the server.
FROM alpine:3

COPY --from=base /garage /usr/local/bin/garage
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
