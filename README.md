craes
=====

craes is a search engine implemented in Python
Compatible with Python 2.7.X

craes uses Redips for its source index and Reknar for its source ranks

To use:
```Python
>>> from craes import Craes
>>> craes = Craes()
```

To do a lucky search:
```Python
>>> craes.lucky_search('foo')
```

To do an ordered search:
```Python
>>> craes.search('bar')
```

To use index or ranks other than the default,

```Python
>>> from craes import Craes
>>> import redips
>>> import reknar
>>> red = redips.load('redips-pickle-file-of-your-choice')
>>> rek = reknar.load('reknar-pickle-file-of-your-choice')
>>> craes = Craes(red.get_index(), rek.get_ranks())
```
