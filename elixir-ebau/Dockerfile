FROM hexpm/elixir:1.19.5-erlang-28.2-debian-bullseye-20260112-slim

WORKDIR /app/

RUN apt-get update -y && \
  apt-get install -y build-essential git curl inotify-tools gnupg && \
  apt-get clean && \
  dpkg --configure -a

COPY . /app/

RUN mix local.hex --force && \
  mix local.rebar --force && \
  mix deps.get

WORKDIR /app/

ENV MIX_OS_DEPS_COMPILE_PARTITION_COUNT=6

RUN mix deps.get

EXPOSE 4000
EXPOSE 4007

CMD ["mix", "phx.server"]

