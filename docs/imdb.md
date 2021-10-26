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

::: phylm.sources.Imdb
    rendering:
      show_source: false
