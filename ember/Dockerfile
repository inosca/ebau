FROM danlynn/ember-cli:3.16.0-node_12.16 as build

COPY package.json yarn.lock /myapp/

RUN yarn install

COPY . /myapp/

ARG KEYCLOAK_URL_ARG
ARG DEPLOY_TARGET

ENV KEYCLOAK_URL=$KEYCLOAK_URL_ARG

RUN yarn deploy $DEPLOY_TARGET

FROM nginx:1.21-alpine

COPY --from=build /myapp/build /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
