FROM danlynn/ember-cli:3.28.5

COPY package.json yarn.lock /myapp/
COPY ./ember-ebau-core/package.json /myapp/ember-ebau-core/

RUN yarn workspace ember-ebau-core install

COPY ember-ebau-core /myapp/ember-ebau-core

WORKDIR /myapp/ember-ebau-core
