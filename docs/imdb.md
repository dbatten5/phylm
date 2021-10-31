# Usage

To access IMDb data points, first ensure you have loaded the IMDb source
through:

```python
phylm.load_source("imdb")
```

Alternatively you can instantiate the IMDb source class directly through:

```python
from phylm.sources import Imdb

imdb = Imdb(raw_title="The Matrix")
```

# Reference

::: phylm.sources.imdb.Imdb
    rendering:
      show_signature_annotations: true
      heading_level: 2
      show_root_heading: false
      show_root_toc_entry: false
