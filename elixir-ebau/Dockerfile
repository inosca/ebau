# Find eligible builder and runner images on Docker Hub. We use Debian instead
# of Alpine to avoid musl DNS-resolution issues (this app uses dns_cluster) and
# BEAM performance regressions under musl.
#
#   - https://hub.docker.com/r/hexpm/elixir/tags - for the build image
#   - https://hub.docker.com/_/debian/tags?name=trixie-20260623-slim - for the release image
#   - Ex: docker.io/hexpm/elixir:1.19.5-erlang-28.2-debian-trixie-20260623-slim
#
ARG ELIXIR_VERSION=1.19.5
ARG OTP_VERSION=28.2
ARG DEBIAN_VERSION=trixie-20260623-slim

ARG BUILDER_IMAGE="docker.io/hexpm/elixir:${ELIXIR_VERSION}-erlang-${OTP_VERSION}-debian-${DEBIAN_VERSION}"
ARG RUNNER_IMAGE="docker.io/debian:${DEBIAN_VERSION}"

FROM ${BUILDER_IMAGE} AS builder

# install build dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential git \
  && rm -rf /var/lib/apt/lists/*

# prepare build dir
WORKDIR /app

# install hex + rebar
RUN mix local.hex --force \
  && mix local.rebar --force

# set build ENV
ENV MIX_ENV="prod"

# install mix dependencies
COPY mix.exs mix.lock ./
RUN mix deps.get --only $MIX_ENV
RUN mkdir config

COPY config/config.exs config/${MIX_ENV}.exs config/
RUN mix deps.compile

# When the LiveView frontend ships to production, uncomment the asset steps
# below (and the `COPY assets` + `mix assets.deploy` further down) and drop the
# standalone `mix phx.digest` — `assets.deploy` already digests. The build then
# needs `ARG APPLICATION` set, since `app-$APPLICATION.scss` is canton-specific.
# RUN mix assets.setup

COPY priv priv

# config/config.exs computes `config :ebau, canton:` from APPLICATION at COMPILE
# time, so it must be present before we compile the app and assemble the release.
# This makes the release image canton-specific, exactly like the Django image.
ARG APPLICATION=demo
ENV APPLICATION=$APPLICATION

# Release version (mix.exs reads EBAU_VERSION). Set by CI from the canton tag;
# defaults to "0.0.0-master" for dev/demo/branch builds.
ARG EBAU_VERSION=0.0.0-master
ENV EBAU_VERSION=$EBAU_VERSION

COPY lib lib

# Compile the release
RUN mix compile

# Digest the few static files we ship (robots.txt, ...) so the endpoint's
# cache_static_manifest is satisfied. No esbuild/sass: the LiveView frontend
# is not shipped to production yet.
RUN mix phx.digest

# LiveView assets (uncomment together with `mix assets.setup` above):
# COPY assets assets
# RUN mix assets.deploy

# Changes to config/runtime.exs don't require recompiling the code
COPY config/runtime.exs config/

COPY rel rel
RUN mix release

# dev: full toolchain image for docker-compose. The source tree is bind-mounted
# and deps/_build live in named volumes; startup (deps.get, migrate, server) is
# handled by entrypoint.dev.sh so code reloading and the asset watchers work.
FROM ${BUILDER_IMAGE} AS dev

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential git inotify-tools postgresql-client \
  && rm -rf /var/lib/apt/lists/*

RUN mix local.hex --force \
  && mix local.rebar --force

ENV MIX_ENV="dev"
WORKDIR /app

EXPOSE 4000

COPY entrypoint.dev.sh /usr/local/bin/entrypoint.dev.sh
RUN chmod +x /usr/local/bin/entrypoint.dev.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.dev.sh"]

# final: slim runtime image containing only the compiled release.
FROM ${RUNNER_IMAGE} AS final

RUN apt-get update \
  && apt-get install -y --no-install-recommends libstdc++6 openssl libncurses6 locales ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Set the locale to Swiss German to match the rest of the stack (Django).
RUN sed -i '/de_CH.UTF-8/s/^# //g' /etc/locale.gen \
  && locale-gen

ENV LANG=de_CH.UTF-8
ENV LANGUAGE=de_CH:de
ENV LC_ALL=de_CH.UTF-8

WORKDIR "/app"
RUN chown nobody /app

# set runner ENV
ENV MIX_ENV="prod"

# Only copy the final release from the build stage
COPY --from=builder --chown=nobody:root /app/_build/${MIX_ENV}/rel/ebau ./

USER nobody

# Run migrations, then start the server.
CMD ["/bin/sh", "-c", "/app/bin/migrate && exec /app/bin/server"]
