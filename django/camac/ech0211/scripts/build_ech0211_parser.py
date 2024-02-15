import itertools
import os.path
import subprocess
import sys

import lxml
import lxml.etree
import requests

SCHEMA_URLS = {
    "http://www.ech.ch/xmlns/eCH-0211/2/eCH-0211-2-0.xsd": "ech_0211_2_0.xsd",
    "http://www.ech.ch/xmlns/eCH-0129/5/eCH-0129-5-0.xsd": "ech_0129_5_0.xsd",
    "http://www.ech.ch/xmlns/eCH-0058/5/eCH-0058-5-0.xsd": "ech_0058_5_0.xsd",
    "http://www.ech.ch/xmlns/eCH-0010/6/eCH-0010-6-0.xsd": "ech_0010_6_0.xsd",
    "http://www.ech.ch/xmlns/eCH-0097/2/eCH-0097-2-0.xsd": "ech_0097_2_0.xsd",
    "http://www.ech.ch/dokument/81ce1f1b-7336-44e7-8e32-269f377e09a4": "ech_0147_t0_1.xsd",
    "http://www.ech.ch/dokument/1a21b2b5-77b9-43ca-a275-59086e3d5a45": "ech_0147_t2_1.xsd",
    "http://www.ech.ch/xmlns/eCH-0044/4/eCH-0044-4-1.xsd": "ech_0044_4_1.xsd",
    "http://www.ech.ch/xmlns/eCH-0007/6/eCH-0007-6-0.xsd": "ech_0007_6_0.xsd",
    "http://www.ech.ch/xmlns/eCH-0008/3/eCH-0008-3-0.xsd": "ech_0008_3_0.xsd",
    "http://www.ech.ch/xmlns/eCH-0044/1/eCH-0044-1-0.xsd": "ech_0044_1_0.xsd",
    "http://www.ech.ch/xmlns/eCH-0046/1/eCH-0046-1-0.xsd": "ech_0046_1_0.xsd",
    "http://www.ech.ch/xmlns/eCH-0010/3/eCH-0010-3-0.xsd": "ech_0010_3_0.xsd",
    "https://share.ech.ch/xmlns/eCH-0039/2/eCH-0039-2-0.xsd": "ech_0039_2_0.xsd",
    "https://share.ech.ch/xmlns/eCH-0039/2/eCH-0039G0T0-1-0.xsd": "ech_0039g0t0_1_0.xsd",
    "http://www.ech.ch/xmlns/eCH-0058/3/eCH-0058-3-0.xsd": "ech_0058_3_0.xsd",
}


def fetch_schema_files(workdir, force):
    files = {}

    for url, schema_file in SCHEMA_URLS.items():
        schema_file = workdir + "/" + schema_file

        # only download xsd file if needed or if it doesn't exist yet
        if force or not os.path.exists(schema_file):
            print(f"Fetching schema from URL {url}")
            resp = requests.get(url)
            schema_content = resp.content

            with open(schema_file, "wb") as schema_fh:
                schema_fh.write(schema_content)
        xsd_as_xml = lxml.etree.parse(schema_file)
        namespace = xsd_as_xml.getroot().attrib["targetNamespace"]

        files[namespace] = schema_file

    return files


def cleanup_xsd_file(schema_file, namespace_file_mapping):
    print(f"Rewriting schema locations to local paths in {schema_file}")
    xsd = lxml.etree.parse(schema_file)

    # some minInclusive are configured with leading zeroes.
    # generateDS simply passes the values to python code, where
    # they are invalid syntax
    # min_inclusives = xsd.findall(
    #    "//xs:minInclusive", namespaces={"xs": "http://www.w3.org/2001/XMLSchema"}
    # )
    # for mi in min_inclusives:
    #    if mi.attrib["value"].startswith("0") and mi.attrib["value"].isnumeric():
    #        mi.attrib["value"] = str(int(mi.attrib["value"]))

    # schema contains invalid values that pyxb can't handle
    enumerations = xsd.findall(
        "//xs:enumeration", namespaces={"xs": "http://www.w3.org/2001/XMLSchema"}
    )
    for en in enumerations:
        value = en.attrib["value"]
        if value.endswith(" "):
            en.attrib["value"] = en.attrib["value"].strip()

    # Update schema location to local file
    for ns, tmp in namespace_file_mapping.items():
        xsd_imports = xsd.findall(
            "xs:import", namespaces={"xs": "http://www.w3.org/2001/XMLSchema"}
        )
        for imp in xsd_imports:
            ns = imp.attrib["namespace"]
            if ns not in namespace_file_mapping:
                print(f"Warning: unknown namespace: {ns}")
            else:
                imp.attrib["schemaLocation"] = os.path.basename(
                    namespace_file_mapping[ns]
                )
        with open(schema_file, "wb") as schema_fh:
            xsd.write(schema_fh, encoding="utf-8")


if __name__ == "__main__":
    workdir = "xsd"
    force = "--force" in sys.argv

    ns_to_file = fetch_schema_files(workdir, force)
    for file in ns_to_file.values():
        cleanup_xsd_file(file, ns_to_file)

    def ns_prefix(ns):
        # luckily, all ech namespaces are of the form
        # http://www.ech.ch/xmlns/ech-XXXX/Y
        # where XXX is the standard, and Y is the version.
        # (some have some sub-version, which we shouldn't drop)
        # Let's convert them to the form echXXX-Y

        ns = ns.replace("http://www.ech.ch/xmlns/", "")
        ns = ns.replace("/", "-")
        ns = ns.lower()
        ns.replace("ech-", "ech")

        return ns

    nsmap = [(ns_prefix(ns), ns) for ns in ns_to_file.keys()]

    nsmap_text = " ".join(f'xmlns:{prefix}="{ns}"' for prefix, ns in nsmap)

    print("Generating python classes from XSD")
    schema_files = ns_to_file.values()
    modules = [
        (
            "-u",
            fn,
            "-m",
            fn.replace("xsd/", "camac.ech0211.schema.").replace(".xsd", ""),
        )
        for fn in schema_files
    ]

    module_args = list(itertools.chain.from_iterable(modules))

    subprocess.check_call(["pyxbgen", "--binding-root=../../", *module_args])
