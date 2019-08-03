# XQL
 Data query language (like jq) modelled on python's list comprehension syntax


## Usage
```python
>>> from xql import XQL
>>> XQL().eval('[e1 for e1 in data]', [0, 1, 2, 3])
[0, 1, 2, 3]
>>> XQL().eval('[e2 for e1 in data for e2 in e1]', [[0, 1, 2], [3, 4]])
[0, 1, 2, 3, 4]
>>> XQL().eval('[e1[0] for e1 in data]', [[0, 1, 2], [3, 4]])
[0, 3]
>>> XQL().eval("[{'val':e1[0]+5} for e1 in data]", [[0, 1, 2], [3, 4]])
[{'val': 5}, {'val': 8}]
```