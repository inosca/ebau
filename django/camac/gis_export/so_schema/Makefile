# GIS export schema tooling for kt_so. See README.md for details.
#
#   make xsd     (re)generate the INTERLIS XSDs from the .ili model (needs docker)
#   make schema  (re)generate the PyXB python bindings from the XSDs (needs pyxb)
#
# `make xsd` downloads the pinned ili2c compiler on demand, so no manual setup
# is required.

ILI2C_VERSION := 5.6.8
ILI2C_FOLDER := ili2c
ILI_MODEL := SO_DSBJD_eBauSO_Geschaefte_20250422
HOST_UID := $(shell id -u)
HOST_GID := $(shell id -g)

.PHONY: all xsd schema
all: xsd schema

# Run ili2c fully inside an ephemeral container: download the pinned compiler,
# compile the .ili model to XSDs, and copy the INTERLIS base + geometry schemas
# out of the distribution (ili2c references but does not emit them).
#
xsd:
	docker run --rm \
		--mount type=bind,source=$(CURDIR),target=/app \
		mcr.microsoft.com/openjdk/jdk:25-ubuntu \
		bash -c " \
			set -eu && \
			apt-get update -qq && apt-get install -y -qq curl >/dev/null && \
			mkdir /opt/$(ILI2C_FOLDER) && cd /opt/$(ILI2C_FOLDER) && \
			curl -sSL https://downloads.interlis.ch/ili2c/ili2c-$(ILI2C_VERSION).zip -o ili2c.zip && \
			jar xf ili2c.zip && \
			cd /app && \
			ILI_CACHE=/opt/.ilicache java -jar /opt/$(ILI2C_FOLDER)/ili2c.jar -oXSD $(ILI_MODEL).ili --out ./xsd && \
			cp /opt/$(ILI2C_FOLDER)/xsd/xtf/2.4/interlis.xsd xsd/INTERLIS.xsd && \
			cp /opt/$(ILI2C_FOLDER)/xsd/xtf/2.4/geometry.xsd xsd/geometry.xsd && \
			chown -R $(HOST_UID):$(HOST_GID) xsd \
		"

schema:
	python build_so_parser.py
