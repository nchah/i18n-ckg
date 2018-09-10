# i18n-ckg scripts/

This repo contains code for the position paper "i18n-CKG: Considerations in Building Internationalization Contextualized Knowledge Graphs" for the Contextualized Knowledge Graphs (CKG 2018) workshop co-located with the International Semantic Web Conference (ISWC 2018).


## Structure

A reference that the repository is structured as follows.

```
$ tree
.
├── README.md
├── demo-data
│   ├── output-demo
│   ├── output-demo-trans-1
│   ├── output-demo-trans-2
│   ├── output-demo-trans-i18nPropScore
│   └── test-query.csv
└── scripts
    ├── README.md
    ├── geckodriver
    ├── s1-collect-data.py
    ├── s2-recon-triples.py
    ├── s3-compile-i18n.py
    └── webdriver-path-demo.txt

```


## Dependencies

The scripts use the following Python libraries, which can be easily installed with `pip`.

- beautifulsoup - Python library for parsing HTML.
- selenium - Python library for browser automation.
	- Other libraries such as `requests` are also possible to use. `selenium` was the most robust solution across the different sites that were looked at.
	- May need to set the path: `$ export PATH=$PATH:/path/to/directory/of/executable/`
	- Note: `pip3 install selenium==3.8.0` may work best until newer versions become more stable.
	- A webdriver is also required to run, e.g. geckodriver from https://www.seleniumhq.org/download/
- translate - Python library for natural language translation.
	- This library utilizes  `MyMemory` as a data source. Other providers can also be set, or a different library may be used.


## Scripts

- s1-collect-data.py - Collects the data from various source websites and outputs triples
- s2-recon-triples.py - Translates the non-English text and provides a CLI tool to reconcile complex triples
- s3-compile-i18n.py - Computes the i18nPropScore metrics as per the paper


## Roadmap

- General TODOs:
	- Adjust scripts to scale with larger inputs (languages, entities)
	- Triples notation to be adjusted to align with standards and other output formats (e.g. JSON-LD)
	- Update license on GitHub
    - Integrate with `rdflib` library or other


