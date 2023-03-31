FROM danlynn/ember-cli:4.8.0 as build

COPY package.json yarn.lock /myapp/
COPY ember-ebau-core/package.json /myapp/ember-ebau-core/
COPY ember-caluma-portal/package.json /myapp/ember-caluma-portal/

RUN yarn workspace caluma-portal install

COPY ember-ebau-core /myapp/ember-ebau-core
COPY ember-caluma-portal /myapp/ember-caluma-portal

WORKDIR /myapp/ember-caluma-portal

ARG APPLICATION
ARG KEYCLOAK_HOST
ARG INTERNAL_URL

RUN yarn deploy production

FROM nginx:1.23-alpine

COPY --from=build /myapp/ember-caluma-portal/build /usr/share/nginx/html
COPY ./ember-caluma-portal/nginx.conf /etc/nginx/conf.d/default.conf
