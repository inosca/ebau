FROM quay.io/keycloak/keycloak:21.0.1 as builder

ENV KC_DB=postgres
ENV KC_HTTP_RELATIVE_PATH=/auth

COPY keycloak-theme-kanton-uri.jar /opt/keycloak/providers/keycloak-theme-kanton-uri.jar

RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:21.0.1

COPY --from=builder /opt/keycloak/ /opt/keycloak/

WORKDIR /opt/keycloak

CMD ["start", "--optimized"]

