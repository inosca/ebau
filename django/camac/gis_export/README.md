# GIS-Export
## SO

The api endpoint returns a xml Transfer File based on the INTERLIS Model supplied by AGI.
The Interlis Model and the schemas are in ./so_schema and need to be updated if the model changes.

Useful Links:
- [Interlis 2 Model]( https://geo.so.ch/modelfinder/modelmetadata?serverUrl=https://geo.so.ch/models&file=DSBJD/SO_DSBJD_eBauSO_Geschaefte_20250422.ili
)
- [Github repo](https://github.com/edigonzales/p-agi_ebauso_rueckfluss):

### Schema generation for kt_so

The schema tooling is in `./so_schema/Makefile` and `./so_schema/build_so_parser.py`.
Run `make` in the `./so_schema` folder to build the xml based on the Interlis model and generate the
python classes. You will need to install the dev dependencies locally for
this to run.
