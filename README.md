# metadataparser

A [TNCPAS-0001][pas] Compatible Metadata Parser Library in Python

[pas]: https://pas.thenewbieclub.my.id/tncpas-0001

## Requirements

* Python 3.7 or newer

We don't use any external dependencies, so you don't need to install any other packages.

## Installation

As the system is not yet published on PyPI, you can install it from the source code:

```bash
pip install -U git+https://github.com/theNewbieClub-MAL/metadataparser.git
```

## Usage

```python
>>> from tncpas_metadata import MetadataParser as MP
>>> # htmlstring is the html string of the page, we use following url as an
>>> # example, and use requests to get the html string
>>> # https://myanimelist.net/forum/?topicid=2045651
>>> metadata = MP(htmlstring)
>>> print(metadata.raw_metadata)
['>>>THM>>SPY X FAMILY',
 '>>>TEM>>🔍',
 '>>>CLR>>#0D0204',
 '>>>STF>>Melissa;Iris;Lumzing;0;0',
 '>>>MAX>>100',
 '>>>LIM>>2|4;3|6;1;0;0',
 '>>>AVA>>6;6;3;0;0']
>>> print(metadata.return_metadata)
{'theme': 'SPY X FAMILY',
 'theme_emoji': '🔍',
 'color': '#0D0204',
 'staff': ['Melissa', 'Iris', 'Lumzing', None, None],
 'maximum': 100,
 'limit': [[2, 4], [3, 6], 1, None, None],
 'available': [6, 6, 3, None, None]}
>>> form = metadata.return_formatted()
EditionMetadata(
    theme='SPY X FA
    MILY',
    maximum=100,
    staffs=[
        StaffEntry(
            nickname='Melissa',
            available=6,
            limit=[2, 4],
            staff_id=None,
            is_allow_slip=True),
        StaffEntry(
            nickname='Iris',
            available=6,
            limit=[3, 6],
            staff_id=None,
            is_allow_slip=True),
        StaffEntry(
            nickname='Lumzing',
            available=3,
            limit=1,
            staff_id=None,
            is_allow_slip=True)],
    theme_id=None,
    theme_emoji='🔍',
    colors=[#0D0204],
    custom=None)
>>> form.colors[0].to_rgb()
(13, 2, 4)
```

## Custom Definition

You can define your own metadata definition during the initialization of the parser:

```python
>>> import datetime
>>> from tncpas_metadata import MetadataParser as MP
>>>
>>> custom_definition = {
... # A dictionary of key-value pairs, where key is the key name, and value is
... #   the definition
... # A key MUST be a string, and value MUST be a dictionary
... # The key name is case-insensitive, and 3 letters long
... "SRT": {
...     # The key name in the returned object, default to the 3 letters key name
...     "key_name": "start",
...
...     # In current version, key_type is a placeholder, will fallback to str,
...     #   int, float, bool, None, and list depending on the value within the
...     #   spec.
...     "key_type": datetime.datetime,
...
...     # If the key is required
...     "required": True,
...
...     # If the key is a list, and total number of items in the list is equal
...     #   to the number of staffs participating
...   # "follow_global_items": True,
...
...     # Comment for the key
...     "description": "Start date of the edition",
... }}
>>> metadata = MP(htmlstring, custom_definition=custom_definition)
>>> parsed = metadata.return_formatted()
>>> print(datetime.datetime.strptime(parsed.custom["start"], "%Y-%m-%d"))
2021-01-01 00:00:00
```

## Exceptions

This parser has 4 exceptions:

1. `ForbiddenListInListError`: Raised when a list of items contains another
   list (e.g. `[[1, 2], 3]`) in the metadata block, except for the `limit` key.
2. `ItemExceedsGlobalLimitError`: Raised when a list of items contains more
   items than the global/staff limit (e.g. 3 items, but the global limit is 1)
3. `MissingRequiredKeyError`: Raised when a required key is missing in the
   metadata block
4. `NoMetadataBlockFoundError`: Raised when no metadata block is found in the
   html string

Other built-in exceptions may be raised during the parsing process, but they are
not handled by the parser.

## Versioning

We use [SemVer](https://semver.org/) for versioning scheme. Below is the
versioning scheme we use:

```text
MAJOR.MINOR.PATCH
```

* `MAJOR`: Incremented when TNCPAS-0001 is updated, or there are breaking changes
* `MINOR`: Incremented when new features are added
* `PATCH`: Incremented when bugs are fixed

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more
information.
