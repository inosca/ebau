FROM gotenberg/gotenberg:8.34-libreoffice

USER root
COPY fonts /usr/local/share/fonts
USER gotenberg

# Only /forms/libreoffice/convert should be enabled
ENV PDFENGINES_DISABLE_ROUTES=true
ENV API_DISABLE_DOWNLOAD_FROM=true
ENV WEBHOOK_DISABLE=true
ENV PROMETHEUS_DISABLE_COLLECT=true
ENV CHROMIUM_DISABLE_ROUTES=true

# No outbound fetches from embedded/linked content
ENV LIBREOFFICE_DENY_PRIVATE_IPS=true
ENV LIBREOFFICE_DENY_PUBLIC_IPS=true

# Warm soffice at boot instead of on first request
ENV LIBREOFFICE_AUTO_START=true
ENV API_TIMEOUT=55s
