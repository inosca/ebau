# stage 1: build keycloak themes using maven
# based on https://docs.docker.com/language/java/build-images/
FROM eclipse-temurin:17-jdk-jammy as theme-builder

WORKDIR /app

COPY themes/.mvn/ .mvn
COPY themes/mvnw themes/pom.xml ./
RUN ./mvnw dependency:resolve

COPY themes/src ./src

RUN ["./mvnw", "deploy"]

# stage 2: build keycloak
FROM quay.io/keycloak/keycloak:21.0.2 as keycloak-builder

ENV KC_DB=postgres
ENV KC_HTTP_RELATIVE_PATH=/auth

COPY themes /tmp/themes
COPY --from=theme-builder /app/target/keycloak-themes-inosca-ebau.jar /opt/keycloak/providers/keycloak-themes-inosca-ebau.jar

RUN /opt/keycloak/bin/kc.sh build

# stage 2: runtime image
FROM quay.io/keycloak/keycloak:21.0.2

COPY --from=keycloak-builder /opt/keycloak/ /opt/keycloak/

WORKDIR /opt/keycloak

ENV KC_DB=postgres
ENV KC_HOSTNAME_STRICT_HTTPS=false
ENV KC_HTTP_ENABLED=true
ENV KC_HTTP_RELATIVE_PATH=/auth
ENV KC_LOG_LEVEL=WARN
ENV KC_PROXY=edge
ENV KEYCLOAK_ADMIN=admin

CMD ["start", "--optimized"]
