FROM danlynn/ember-cli:4.12.1 as build

COPY package.json yarn.lock /myapp/
COPY ember-ebau-core/package.json /myapp/ember-ebau-core/
COPY ember-camac-ng/package.json /myapp/ember-camac-ng/

RUN --mount=type=cache,target=.yarn \
  YARN_CACHE_FOLDER=.yarn \
  yarn workspace camac-ng install

COPY ember-ebau-core /myapp/ember-ebau-core
COPY ember-camac-ng /myapp/ember-camac-ng

WORKDIR /myapp/ember-camac-ng

ARG APPLICATION
ARG APP_ENV

RUN yarn deploy production

FROM nginxinc/nginx-unprivileged:1.25-alpine

COPY --from=build /myapp/ember-camac-ng/build /usr/share/nginx/html
COPY ./ember-camac-ng/nginx.conf /etc/nginx/conf.d/default.conf
