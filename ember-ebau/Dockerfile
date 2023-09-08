FROM danlynn/ember-cli:4.8.0 as build

COPY package.json yarn.lock /myapp/
COPY ember-ebau-core/package.json /myapp/ember-ebau-core/
COPY ember-ebau/package.json /myapp/ember-ebau/

RUN --mount=type=cache,target=.yarn \
  YARN_CACHE_FOLDER=.yarn \
  yarn workspace ebau install

COPY ember-ebau-core /myapp/ember-ebau-core
COPY ember-ebau /myapp/ember-ebau

WORKDIR /myapp/ember-ebau

ARG APPLICATION
ARG KEYCLOAK_HOST
ARG PORTAL_URL
ARG SO_GIS_URL

RUN yarn deploy production

# Currently only used by SO
FROM nginxinc/nginx-unprivileged:1.25-alpine as env-prod

COPY --from=build /myapp/ember-ebau/build /usr/share/nginx/html
COPY nginx/ember.conf /etc/nginx/conf.d/default.conf
COPY nginx/replace-env-vars.sh /usr/local/bin/replace-env-vars

CMD /bin/sh -c "replace-env-vars '\${KEYCLOAK_HOST},\${PORTAL_URL},\${SO_GIS_URL}' /usr/share/nginx/html && nginx -g 'daemon off;'"

FROM nginxinc/nginx-unprivileged:1.25-alpine

COPY --from=build /myapp/ember-ebau/build /usr/share/nginx/html
COPY ./ember-ebau/nginx.conf /etc/nginx/conf.d/default.conf
