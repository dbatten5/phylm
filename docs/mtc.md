# Usage

To access Metacritic data points, first ensure you have loaded the Metacritic source
through:

```python
await phylm.load_source("mtc")
```

Alternatively you can instantiate the Metacritic source class directly through:

```python
from phylm.sources import Mtc

mtc = Mtc(raw_title="The Matrix", raw_year=1999)  # raw_year is optional
await mtc.load_source()
```

# Reference

::: phylm.sources.mtc.Mtc
    rendering:
      show_signature_annotations: true
      heading_level: 2
      show_root_heading: false
      show_root_toc_entry: false
