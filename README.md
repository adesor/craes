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

To use index or ranks other than the default,
```Python
>>> from craes import Craes
>>> import redips
>>> import reknar
>>> red = redips.load('redips-pickle-file-of-your-choice')
>>> rek = reknar.load('reknar-pickle-file-of-your-choice')
>>> craes = Craes(red.get_index(), rek.get_ranks())
```

To do a lucky search:
```Python
>>> craes.lucky_search('foo')
http://abc.xyz
```

To do an ordered search:
```Python
>>> craes.search('bar')
http://foo.bar
http://blah.bleh
```

To fetch the best result:
```Python
>>> craes.get_best('foo')
'http://abc.xyz'
```

To fetch an ordered list of all the search results:
```Python
>>> craes.get_results('bar')
['http://foo.bar', 'http://abc.xyz']
```


