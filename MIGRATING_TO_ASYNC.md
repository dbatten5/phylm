# Migrating to async

Version `5.0.0` introduces some breaking changes, most notably moving the `load_source`
and `load_sources` methods on the `Phylm` class to async. The main motivation for this
change is to improve the performance of `load_sources` and also to allow the users of
this package to make further performance gains in their own applications.

By moving to async, the time taken to run `load_sources` on 3 sources (`imdb`, `mtc` and
`rt`) has decreased from 4-5 seconds down to less than 3 (pretty much the time taken to
fetch just the `imdb` source).

However, in order to use these async methods, some changes need to be made to any code
invoking them. It's recommended to read up on `async` Python, eg. using the `asyncio`
library and make the changes as you see fit. If you're in a hurry though take a look at
the example below.

## Example

Consider the following script using `phylm < 5.0.0`:

```python
from phylm import Phylm

def main():
    p = Phylm("The Matrix")
    p.load_sources(["imdb", "mtc", "rt"])
    print(f"Imdb: {p.imdb.rating}, Mtc: {p.mtc.rating}, Rt: {p.rt.tomato_score}")

if __name__ == "__main__":
    main()
```

To use the async API in `phylm >= 5.0.0`, the simplest change needed is to just use the
`await` keyword:

```python
import asyncio
from phylm import Phylm

async def main():
    p = Phylm("The Matrix")
    await p.load_sources(["imdb", "mtc", "rt"])
    print(f"Imdb: {p.imdb.rating}, Mtc: {p.mtc.rating}, Rt: {p.rt.tomato_score}")

if __name__ == "__main__":
    asyncio.run(main())
```

Note that the `await` keyword must be used inside a `async` function. In order to run an
`async` function (in this case `main()`), it needs to be run in an _event loop_.
`asyncio.run()` is a nice wrapper around this functionality. If you're using `phylm` as
part of an web application with async support, eg. `FastAPI`/`starlette`, you likely
wouldn't need to explicitly run `asyncio.run()` as this would be handled by the
framework.
