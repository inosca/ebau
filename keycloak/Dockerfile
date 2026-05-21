ARG VERSION=25.0

# stage 1: build keycloak themes using maven
# based on https://docs.docker.com/language/java/build-images/
FROM eclipse-temurin:17-jdk-jammy AS builder

WORKDIR /theme

COPY themes/.mvn/ .mvn
COPY themes/mvnw themes/pom.xml ./
RUN ./mvnw dependency:resolve

COPY themes/src ./src

RUN ["./mvnw", "deploy"]

WORKDIR /spi-sms

COPY themes/.mvn/ .mvn
COPY themes/mvnw keycloak-2fa-sms-authenticator/pom.xml ./
RUN ./mvnw dependency:resolve

COPY keycloak-2fa-sms-authenticator/src ./src

RUN ["./mvnw", "package"]

# stage 1b: build spi-token (only used in keycloak-v26)
FROM eclipse-temurin:17-jdk-jammy AS builder-token

WORKDIR /spi-token

COPY themes/.mvn/ .mvn
COPY themes/mvnw ebau-token-exchange/pom.xml ./
RUN ./mvnw dependency:resolve

COPY ebau-token-exchange/src ./src

RUN ["./mvnw", "package"]

# stage 2: build and run image
# Sadly, we can't separate the build and run stages because we need the
# distributed cache config (which happens during build time) to be configurable
# via environment variables.
FROM quay.io/keycloak/keycloak:${VERSION} AS keycloak-builder

ENV KC_DB=postgres
ENV KC_HTTP_RELATIVE_PATH=/auth
ENV KC_HTTP_ENABLED=true
ENV KC_HTTP_RELATIVE_PATH=/auth
ENV KC_LOG_LEVEL=warn
ENV KC_PROXY_HEADERS=xforwarded
ENV KC_CACHE_CONFIG_FILE=cache-ispn-tcpstatic.xml
ENV KC_TRANSACTION_XA_ENABLED=false

ENV KCISPN_LISTEN_ADDR=127.0.0.1
ENV KCISPN_BIND_PORT=7800
ENV KCISPN_HOSTS=localhost[7800]

COPY themes /tmp/themes
COPY --from=builder /theme/target/keycloak-themes-inosca-ebau.jar /opt/keycloak/providers/keycloak-themes-inosca-ebau.jar
COPY --from=builder /spi-sms/target/dasniko.keycloak-2fa-sms-authenticator.jar /opt/keycloak/providers/dasniko.keycloak-2fa-sms-authenticator.jar
COPY cache-ispn-tcpstatic.xml /opt/keycloak/conf/cache-ispn-tcpstatic.xml

COPY custom-entrypoint.sh /opt/keycloak/bin/
ENTRYPOINT ["/opt/keycloak/bin/custom-entrypoint.sh"]
CMD ["start", "--optimized"]

# currently we have two versions of keycloak running, v25 and v26, so we need to
# create two different build targets until all cantons are upgraded.
# this is because the ENV `KC_HOSTNAME_STRICT_HTTPS` should be removed for v26.
# a canton that uses v26 should use the keycloak-v26 build target to stop early.
#
# compose file reference:
#
# ````
#   keycloak:
#     build:
#       context: ../keycloak
#       args:
#         VERSION: 26.2
#       target: keycloak-v26
# ````
FROM keycloak-builder AS keycloak-v26

COPY --from=builder-token /spi-token/target/inosca.ebau-token-exchange.jar /opt/keycloak/providers/inosca.ebau-token-exchange.jar

# For existing cantons that are not upgraded yet we use the keycloak-v25 build target
# to still add the ENV variable.
# since this is the last target this will be the default, so no changes are needed
# in the compose files.
#
# compose file reference:
#
# ````
#   keycloak:
#     build:
#       context: ../keycloak
# ````
FROM keycloak-builder AS keycloak-v25

ENV KC_HOSTNAME_STRICT_HTTPS=false
