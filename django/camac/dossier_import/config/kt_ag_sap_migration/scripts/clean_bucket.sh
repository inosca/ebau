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

echo "Delete all files in bucket ${STORAGE}:${BUCKET} (y|n)?"
read CONFIRMATION

if [ "$CONFIRMATION" = 'y' ]
then
  rclone delete "${STORAGE}:${BUCKET}" --fast-list --transfers=32 --checkers=16 --progress
fi

