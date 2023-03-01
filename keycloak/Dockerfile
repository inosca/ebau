FROM quay.io/keycloak/keycloak:20.0.5 as builder

ENV KC_DB=postgres
ENV KC_HTTP_RELATIVE_PATH=/auth

RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:20.0.5

COPY --from=builder /opt/keycloak/ /opt/keycloak/

WORKDIR /opt/keycloak

ENV KC_DB=postgres
ENV KC_HOSTNAME_STRICT_HTTPS=false
ENV KC_HTTP_ENABLED=true
ENV KC_HTTP_RELATIVE_PATH=/auth
ENV KC_LOG_LEVEL=WARN
ENV KC_PROXY=edge
ENV KEYCLOAK_ADMIN=admin

CMD ["start", "--optimized"]
