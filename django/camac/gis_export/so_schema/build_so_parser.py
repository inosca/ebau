"""Generate PyXB python bindings from the INTERLIS XSD schemas.

The XSDs are produced from the `.ili` model by the `make xsd` target (see
README.md). This script turns them into importable python classes under
`camac.gis_export.so_schema`, mirroring the approach used in `camac.ech0211`.

Unlike the eCH schemas, the INTERLIS XSDs emit `<xsd:import>` elements without a
`schemaLocation`, so a single-file `pyxbgen` run cannot resolve the imported
namespaces (that is why running pyxbgen on the model XSD alone fails with
"NamespaceError: ... has no category attributeDeclaration"). We therefore hand
*every* schema - including the INTERLIS base and geometry schemas that ship with
the ili2c compiler - to one pyxbgen invocation so all namespaces resolve
together.

Run via `make schema` from the gis_export/so_schema/ directory.
"""

import subprocess
from itertools import chain
from pathlib import Path

SCHEMA_SRC_DIR = Path("xsd")
BINDING_PACKAGE = "camac.gis_export.so_schema"

# pyxbgen resolves all schemas in a single run regardless of order, but listing
# the base and imported namespaces before the dependent model schema keeps the
# run deterministic. Anything not listed here (e.g. a future model schema) is
# appended afterwards.
SCHEMA_ORDER = [
    "INTERLIS",
    "geometry",
    "Units",
    "CoordSys",
    "Geometry_V2",
    "GeometryCHLV95_V2",
    "GeometryCHLV03_V2",
]


def ordered_schema_files():
    by_stem = {f.stem: f for f in sorted(SCHEMA_SRC_DIR.glob("*.xsd"))}

    ordered = [by_stem.pop(stem) for stem in SCHEMA_ORDER if stem in by_stem]
    # the remaining schema(s) - the model itself - come last so that their
    # imports are already registered when they are resolved
    ordered += [by_stem[stem] for stem in sorted(by_stem)]
    return ordered


def main():
    if not SCHEMA_SRC_DIR.is_dir():
        raise SystemExit(
            f"{SCHEMA_SRC_DIR}/ not found - run this from django/camac/gis_export/so_schema/"
        )

    module_args = list(
        chain.from_iterable(
            ("-u", str(xsd), "-m", f"{BINDING_PACKAGE}.{xsd.stem}")
            for xsd in ordered_schema_files()
        )
    )

    print("Generating python bindings from XSD into camac/gis_export/so_schema/")
    subprocess.check_call(["pyxbgen", "--binding-root=../../../", *module_args])


if __name__ == "__main__":
    main()
