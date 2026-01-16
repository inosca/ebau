FROM hexpm/elixir:1.19.5-erlang-28.2-debian-bullseye-20260112-slim

WORKDIR /app/

RUN apt-get update -y && \
  apt-get install -y build-essential git curl inotify-tools gnupg && \
  apt-get clean && \
  dpkg --configure -a

# Install Node.js (via NodeSource)
# This is only necessary because of uikit. I would love to get rid of this.
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
  && apt-get install -y nodejs \
  && npm install -g npm@latest

COPY . /app/

RUN mix local.hex --force && \
  mix local.rebar --force && \
  mix deps.get

WORKDIR /app/

RUN MIX_OS_DEPS_COMPILE_PARTITION_COUNT=$(($(nproc) / 2)) mix deps.get

EXPOSE 4000
EXPOSE 4007

CMD ["mix", "phx.server"]

