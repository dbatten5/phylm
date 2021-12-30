# Usage

To access Rotten Tomatoes data points, first ensure you have loaded the Rotten Tomatoes source
through:

```python
await phylm.load_source("rt")
```

Alternatively you can instantiate the Rotten Tomatoes source class directly through:

```python
from phylm.sources import Rt

rot_tom = Rt(raw_title="The Matrix", raw_year=1999)  # raw_year is optional
await rot_tom.load_source()
```

# Reference

::: phylm.sources.rt.Rt
    rendering:
      show_signature_annotations: true
      heading_level: 2
      show_root_heading: false
      show_root_toc_entry: false
