#!/usr/bin/env bash
source ./ebau.env;
if [ -z "$KEYCLOAK_HOST" ]; then
  echo "Hostname of eBau Keycloak (Local: http://ebau-keycloak.localhost): ";
  read KEYCLOAK_HOST;
  echo "KEYCLOAK_HOST=$KEYCLOAK_HOST" >> ./ebau.env;
fi;
if [ -z "$EBAU_HOST" ]; then
  echo "Hostname of eBau (Local: http://ember-ebau.localhost): ";
  read EBAU_HOST;
  echo "EBAU_HOST=$EBAU_HOST" >> ./ebau.env;
fi;
if [ -z "$GIS_EXPORT_SECRET" ]; then
  echo "gis_export Secret (Local: http://ebau-keycloak.localhost/auth/admin/master/console/#/ebau/clients/23f8991e-8b25-4f4d-b6b2-1d1447005817/credentials): ";
  read GIS_EXPORT_SECRET;
  echo "GIS_EXPORT_SECRET=$GIS_EXPORT_SECRET" >> ./ebau.env;
fi;


FOLDER="gis_export_test_$(date +"%Y_%m_%d_%I_%M_%S")"
mkdir $FOLDER

curl -v --request POST \
--url "$KEYCLOAK_HOST/auth/realms/ebau/protocol/openid-connect/token" \
--header 'content-type: application/x-www-form-urlencoded' \
--data grant_type=client_credentials \
--data scope=openid \
--data client_id=sogis \
--data client_secret=$GIS_EXPORT_SECRET \
> $FOLDER/token.json

TOKEN=$(cat $FOLDER/token.json | sed -nE 's/.*access_token":"([^"]+)".*/\1/p')
echo "Token: $TOKEN"
curl -v -L "$EBAU_HOST/api/v1/gis-export/so/" \
-H "authorization: Bearer $TOKEN" \
> $FOLDER/export.xtf

