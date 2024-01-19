# Metacritic

## Usage

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

## Reference

```{eval-rst}
.. autoclass:: phylm.sources.mtc.Mtc
   :members:
```
