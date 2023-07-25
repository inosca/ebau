#!/bin/sh

# Configure mc to connect to our minio container
mc config host add dc-minio http://minio:9000 $MINIO_ACCESS_KEY $MINIO_SECRET_KEY --api S3v4;
# Only run if this is the initial setup
if [ "$1" != "-u" ]; then
  # Create buckets for alexandria and DMS
  mc mb -p dc-minio/dms-media;
  mc mb -p dc-minio/alexandria-media;
  # Setup alexandria callback
  mc event add dc-minio/alexandria-media arn:minio:sqs::ALEXANDRIA:webhook -p --event put;
fi
# Copy DMS default templates to dms-media bucket
mc cp /tmp/dms-media/* dc-minio/dms-media/;
