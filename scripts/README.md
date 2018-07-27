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
    └── webdriver-path.txt

```


## Dependencies

- selenium - Python library for browser automation.
	- Note: `pip3 install selenium==3.8.0` may work best until newer versions become more stable.
	- a webdriver, e.g. geckodriver from https://www.seleniumhq.org/download/
- translate - Python library for natural language translation.


## scripts

- s1-collect-data.py
- s2-recon-triples.py
- s3-compile-i18n.py

