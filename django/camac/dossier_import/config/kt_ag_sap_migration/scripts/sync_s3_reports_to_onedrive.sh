#!/bin/bash

if [ -z "$1" ]
then
  echo usage: $0 '(stage|prod)' '[dir-to-sync]'
  exit 1
fi

ENV="$1"

if [ "$ENV" = 'stage' ]
then
  BUCKET=diba-stage-migration-media
  STORAGE=s3-stage
elif [ "$ENV" = 'prod' ]
then
  BUCKET=diba-prod-migration-media
  STORAGE=s3-prod
else
  echo unsupported environment: $1
  exit 1
fi

if [ -n "$2" ]
then
  REPORT_DIR="$2"
fi

DEST=/c/Users/emarhub002/Kanton\ Aargau/DIBA\ -\ Projektdokumente/50\ Realisierung/Migration/Reports
SOURCE=app/kt_ag/migration_reports

if [ -z "$REPORT_DIR" ]
then
  rclone lsf ${STORAGE}:${BUCKET}/${SOURCE}

  echo -n "Enter Dir to sync: "
  read REPORT_DIR
fi

FULL_SOURCE="${STORAGE}:${BUCKET}/${SOURCE}/${REPORT_DIR}"
FULL_DEST="${DEST}/${REPORT_DIR}_${ENV}"

rclone copy "$FULL_SOURCE" "$FULL_DEST" --progress

echo "Done copying \"$FULL_SOURCE\" to \"$FULL_DEST\" "
