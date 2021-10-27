# Usage

To access Metacritic data points, first ensure you have loaded the Metacritic source
through:

```python
phylm.load_source("mtc")
```

Alternatively you can instantiate the Metacritic source class directly through:

```python
from phylm.sources import Mtc

mtc = Mtc(raw_title="The Matrix")
```

# Reference

::: phylm.sources.mtc.Mtc
    rendering:
      show_source: false
