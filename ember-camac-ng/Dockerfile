FROM danlynn/ember-cli:4.8.0 as build

COPY package.json yarn.lock /myapp/
COPY ember-ebau-core/package.json /myapp/ember-ebau-core/
COPY ember-camac-ng/package.json /myapp/ember-camac-ng/

RUN yarn workspace camac-ng install

COPY ember-ebau-core /myapp/ember-ebau-core
COPY ember-camac-ng /myapp/ember-camac-ng

WORKDIR /myapp/ember-camac-ng

ARG APPLICATION

RUN yarn deploy production

FROM nginx:1.23-alpine

COPY --from=build /myapp/ember-camac-ng/build /usr/share/nginx/html
COPY ./ember-camac-ng/nginx.conf /etc/nginx/conf.d/default.conf
