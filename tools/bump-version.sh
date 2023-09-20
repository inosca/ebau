#!/bin/bash

VERSION=$1

if [ -z $VERSION ]
  then echo "Please pass a version"
  exit 1
fi

echo $VERSION > VERSION.txt;
sed -i -e "s/\"version\": \".*\",/\"version\": \"$VERSION\",/g" ember-camac-ng/package.json
sed -i -e "s/\"version\": \".*\",/\"version\": \"$VERSION\",/g" ember-caluma-portal/package.json
sed -i -e "s/__version__ = \".*\"/__version__ = \"$VERSION\"/g" django/camac/camac_metadata.py
