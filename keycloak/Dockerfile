# stage 1: build keycloak themes using maven
# based on https://docs.docker.com/language/java/build-images/
FROM eclipse-temurin:17-jdk-jammy as theme-builder

WORKDIR /app

COPY themes/.mvn/ .mvn
COPY themes/mvnw themes/pom.xml ./
RUN ./mvnw dependency:resolve

COPY themes/src ./src

RUN ["./mvnw", "deploy"]

# stage 2: runtime image (that also builds keycloak)
FROM quay.io/keycloak/keycloak:21.0.2 as keycloak-builder

ENV KC_DB=postgres
ENV KC_HTTP_RELATIVE_PATH=/auth
ENV KC_HOSTNAME_STRICT_HTTPS=false
ENV KC_HTTP_ENABLED=true
ENV KC_HTTP_RELATIVE_PATH=/auth
ENV KC_LOG_LEVEL=warn
ENV KC_PROXY=edge
ENV KC_CACHE_CONFIG_FILE=cache-ispn-tcpstatic.xml
ENV KC_TRANSACTION_XA_ENABLED=false

COPY themes /tmp/themes
COPY --from=theme-builder /app/target/keycloak-themes-inosca-ebau.jar /opt/keycloak/providers/keycloak-themes-inosca-ebau.jar

COPY cache-ispn-tcpstatic.xml /opt/keycloak/conf/cache-ispn-tcpstatic.xml

COPY custom-entrypoint.sh /opt/keycloak/bin/
ENTRYPOINT ["/opt/keycloak/bin/custom-entrypoint.sh"]
CMD ["start", "--optimized"]
