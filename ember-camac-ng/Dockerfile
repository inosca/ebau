FROM danlynn/ember-cli:latest as build

ARG APPLICATION

COPY package.json yarn.lock /myapp/

RUN yarn install

COPY . /myapp/

RUN yarn deploy production

FROM nginx:alpine

COPY --from=build /myapp/build /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
