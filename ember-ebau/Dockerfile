FROM danlynn/ember-cli:3.28.5 as build

ARG APPLICATION
ARG KEYCLOAK_HOST
ARG INTERNAL_URL

COPY package.json yarn.lock /myapp/
COPY ember-ebau-core /myapp/ember-ebau-core
COPY ./ember-ebau/package.json /myapp/ember-ebau/

RUN yarn workspace ebau install

COPY ember-ebau /myapp/ember-ebau

WORKDIR /myapp/ember-ebau
RUN yarn deploy production

FROM nginx:1.21-alpine

COPY --from=build /myapp/ember-ebau/build /usr/share/nginx/html
COPY ./ember-ebau/nginx.conf /etc/nginx/conf.d/default.conf
