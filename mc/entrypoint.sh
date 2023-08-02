#!/bin/sh

# Configure mc to connect to our minio container
mc config host add dc-minio http://minio:9000 $MINIO_ACCESS_KEY $MINIO_SECRET_KEY --api S3v4;
# Only run if this is the initial setup
if [ "$1" != "-u" ]; then
  # Create bucket for DMS
  mc mb -p dc-minio/dms-media;

  # Create bucket and event for alexandria
  # TODO: GR must make rename their alexandria bucket and event to
  # alexandria-media instead of caluma-media
  if [ "$APPLICATION" == "kt_gr" ]; then
    mc mb -p dc-minio/caluma-media;
    mc event add dc-minio/caluma-media arn:minio:sqs::CALUMA:webhook -p --event put;
  else
    mc mb -p dc-minio/alexandria-media;
    mc event add dc-minio/alexandria-media arn:minio:sqs::ALEXANDRIA:webhook -p --event put;
  fi
fi
# Copy DMS default templates to dms-media bucket
mc cp /tmp/dms-media/* dc-minio/dms-media/;
