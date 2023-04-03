FROM quay.io/keycloak/keycloak:21.0.2 as builder

ENV KC_DB=postgres
ENV KC_HTTP_RELATIVE_PATH=/auth

COPY keycloak-theme-kanton-schwyz.jar /opt/keycloak/providers/keycloak-theme-kanton-schwyz.jar

RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:21.0.2
COPY --from=builder /opt/keycloak/ /opt/keycloak/

WORKDIR /opt/keycloak

CMD ["start", "--optimized"]