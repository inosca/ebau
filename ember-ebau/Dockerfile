FROM danlynn/ember-cli:4.8.0 as build

COPY package.json yarn.lock /myapp/
COPY ember-ebau-core/package.json /myapp/ember-ebau-core/
COPY ember-ebau/package.json /myapp/ember-ebau/

RUN yarn workspace ebau install

COPY ember-ebau-core /myapp/ember-ebau-core
COPY ember-ebau /myapp/ember-ebau

WORKDIR /myapp/ember-ebau

ARG APPLICATION
ARG KEYCLOAK_HOST
ARG INTERNAL_URL

RUN yarn deploy production

FROM nginx:1.25-alpine

COPY --from=build /myapp/ember-ebau/build /usr/share/nginx/html
COPY ./ember-ebau/nginx.conf /etc/nginx/conf.d/default.conf
