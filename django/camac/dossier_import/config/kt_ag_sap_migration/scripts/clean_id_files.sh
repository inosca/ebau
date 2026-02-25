#!/bin/bash

if [ -z "$2" ]
then
  echo usage: $0 '(stage|prod)' '(alexandria|dms|migration)'
  exit 1
fi

if [ $1 = 'stage' ]
then
  BUCKET=diba-stage-${2}-media
  STORAGE=s3-stage
elif [ $1 = 'prod' ]
then
  BUCKET=diba-prod-${2}-media
  STORAGE=s3-prod
else
  echo unsupported environment: $1
  exit 1
fi

echo Found the following files:
  rclone lsf "${STORAGE}:${BUCKET}" -R \
    --filter "+ */000000*" \
    --filter "- *" \
    --files-only

echo "See the found file above."
echo "Delete all those files in bucket ${STORAGE}:${BUCKET} (y|n)?"
read CONFIRMATION

if [ "$CONFIRMATION" = 'y' ]
then
  rclone delete "${STORAGE}:${BUCKET}" \
    --filter "+ */000000*" \
    --filter "- *" \
    --transfers 32 --checkers 64
fi

