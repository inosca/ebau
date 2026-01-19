FROM node:20 AS node-builder

WORKDIR /opt/
COPY ./assets/package*.json /opt/
RUN npm install

FROM hexpm/elixir:1.19.5-erlang-28.2-debian-bullseye-20260112-slim AS build

WORKDIR /app/

RUN apt-get update -y && \
  apt-get install -y build-essential git curl inotify-tools gnupg && \
  apt-get clean && \
  dpkg --configure -a

COPY . /app/
COPY --from=node-builder /opt/node_modules /opt/node_modules
RUN ln -sf /opt/node_modules /app/assets/node_modules

RUN mix local.hex --force && \
  mix local.rebar --force && \
  mix deps.get

WORKDIR /app/

RUN MIX_OS_DEPS_COMPILE_PARTITION_COUNT=$(($(nproc) / 2)) mix deps.get

EXPOSE 4000
EXPOSE 4007

CMD ["mix", "phx.server"]
