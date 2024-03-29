# Rotten Tomatoes

## Usage

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

## Reference

```{eval-rst}
.. autoclass:: phylm.sources.rt.Rt
   :members:
```
