This is the main entrypoint class.

# Usage

First instantiate the class with a `title` property:

```python
from phylm import Phylm

p = Phylm(title="The Matrix")
```

Next load a source through either `load_sources` or `load_source`:

```python
p.load_sources(["imdb", "rt"])
p.load_source("mtc")
```

Now the source will be available through a property of the same name:

```python
>>> p.imdb
<phylm.sources.imdb.Imdb object at 0x108a94810>
```

See the docs for a source for a full list of the available data points.

# Reference

::: phylm.Phylm
    rendering:
      show_source: true
