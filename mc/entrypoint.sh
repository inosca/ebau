#!/bin/sh

# Configure mc to connect to our minio container
mc config host add dc-minio http://minio:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD --api S3v4;
# Only run if this is the initial setup
if [ "$1" != "-u" ]; then
  # Create buckets for DMS and alexandria
  mc mb -p dc-minio/dms-media;
  mc mb -p dc-minio/alexandria-media;
fi
# Copy DMS default templates to dms-media bucket
mc cp /tmp/dms-media/* dc-minio/dms-media/;
