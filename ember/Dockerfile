FROM node:8

# Install nginx
RUN \
 apt-get update && \
 apt-get install -y --no-install-recommends nginx && \
 rm -rf /var/lib/apt/lists/* && \
 rm /var/www/html/index.nginx-debian.html && \
 ln -sf /dev/stdout /var/log/nginx/access.log && \
 ln -sf /dev/stderr /var/log/nginx/error.log

# Install chrome for testing
# TODO: run tests in a chromium container
# https://hub.docker.com/r/markadams/chromium-xvfb/
RUN \
  wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
  echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
  apt-get update && \
  apt-get install -y --no-install-recommends google-chrome-stable && \
  rm -rf /var/lib/apt/lists/*

COPY . /app
COPY ./nginx.conf /etc/nginx/sites-enabled/default

WORKDIR /app

# Install deps and build app with mock API
RUN \
 yarn && \
 yarn build -prod

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
