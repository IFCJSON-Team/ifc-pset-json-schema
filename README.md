# ifc-pset-json-schema
This repository captures initial experiments porting IFC's PSet XML definitions to JSON Schema. It contains four major parts:
- `getpset.py`: pulls PSD-XML files from BuildingSmart and deposits them in `psets/xml`
- `model.py`: a small abstraction layer for property sets. Includes JSON serialization-specific code and associated type predicates.
- `pset2json.py`: The core script that performs the translation. If run as a command-line script, output will be directed to `psets/json`. Assumes `getpsets.py` has already run.
- `psets-vocabulary.json`: A extension JSON Schema meta-schema capturing annotations present in PSD-XML (`ifcversion` and `datatype` for now)

## Next Steps
This exercise has demonstrated some of the limitations of JSON Schema for fully capturing IFC PSet data. Unresolved issues include:
- Defining model types and JSON serializations for ReferenceValues and TableValues.
- Figuring out what to do for internationalization support. JSON Schema itself [seems to have no direct internationalization support](https://github.com/json-schema-org/json-schema-spec/issues/53).
- Figuring out how address PSD-XML's name and definition aliases.
- Adding regression tests to ensure the output corresponds to the PSD-XML input.

