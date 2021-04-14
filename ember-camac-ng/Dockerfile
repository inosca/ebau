FROM danlynn/ember-cli:3.20.0 as build

ARG APPLICATION

COPY package.json yarn.lock /myapp/
COPY ./ember-camac-ng/package.json ./ember-camac-ng/yarn.lock /myapp/ember-camac-ng/

RUN yarn workspace camac-ng install

COPY ember-camac-ng /myapp/ember-camac-ng

WORKDIR /myapp/ember-camac-ng
RUN yarn deploy production

FROM nginx:alpine

COPY --from=build /myapp/ember-camac-ng/build /usr/share/nginx/html
COPY ./ember-camac-ng/nginx.conf /etc/nginx/conf.d/default.conf
