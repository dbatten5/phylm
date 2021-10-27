# Usage

To access Rotten Tomatoes data points, first ensure you have loaded the Rotten Tomatoes source
through:

```python
phylm.load_source("rt")
```

Alternatively you can instantiate the Rotten Tomatoes source class directly through:

```python
from phylm.sources import Rt

rot_tom = Rt(raw_title="The Matrix")
```

# Reference

::: phylm.sources.rt.Rt
    rendering:
      show_source: false