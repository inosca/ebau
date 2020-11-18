FROM danlynn/ember-cli:3.20.0 as build

COPY package.json yarn.lock /myapp/

RUN yarn install

COPY . /myapp/

RUN yarn deploy production

FROM nginx:alpine

COPY --from=build /myapp/build /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
