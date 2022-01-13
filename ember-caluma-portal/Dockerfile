FROM danlynn/ember-cli:3.28.5 as build

ARG APPLICATION
ARG KEYCLOAK_HOST

COPY package.json yarn.lock /myapp/
COPY ember-ebau-core /myapp/ember-ebau-core
COPY ./ember-caluma-portal/package.json /myapp/ember-caluma-portal/

RUN yarn workspace caluma-portal install

COPY ember-caluma-portal /myapp/ember-caluma-portal

WORKDIR /myapp/ember-caluma-portal
RUN yarn deploy production

FROM nginx:alpine

COPY --from=build /myapp/ember-caluma-portal/build /usr/share/nginx/html
COPY ./ember-caluma-portal/nginx.conf /etc/nginx/conf.d/default.conf
