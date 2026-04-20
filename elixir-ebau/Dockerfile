FROM hexpm/elixir:1.19.5-erlang-28.2-debian-bullseye-20260112-slim AS build

WORKDIR /app/

RUN apt-get update -y && \
  apt-get install -y build-essential git curl inotify-tools gnupg && \
  apt-get clean && \
  dpkg --configure -a

RUN mix local.hex --force && \
  mix local.rebar --force

COPY mix.exs mix.lock ./
RUN mix deps.get

COPY . /app/

EXPOSE 4000
EXPOSE 4007

ENTRYPOINT ["/entrypoint.sh"]
