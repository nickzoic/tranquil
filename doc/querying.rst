==========
 TRANQUIL
==========


Querying
========

Context
-------

Who are you and what do you want.

Actions
-------

An action is either just an action_name or a list of action_name and some parameters.

Example actions::

    'all'

    'count'

    [ 'filter', { ... } ]

    [ 'before', '2011-12-13' ]

Action Lists
------------

An action list is a list of actions, which compose left to right.

Example action_lists::

    [ 'count' ]

    [ [ 'filter', { 'is_author': true } ], 'count' ]

Action Groups
-------------

An action group labels actions and runs them in parallel in the same context.

The structure is { action_label: action_list }
As a special case, if the righthand side is a string it is assumed to be an action_name::

    {
        'count': 'count',
        'page': [ 'page', 0, 5 ] 
    }

The Action Labels are a convenience to the frontend programmer:
they are used to construct a response.  For example, the above
query returns something like::

    {
         'count': 107,
         'page': [ {...}, {...}, {...}, {...}, {...} ]
    }

... so that you can conveniently refer to ``response.count`` and 
``response.page[n]`` from javascript.

Action groups nest::

    { 
        'authors': [
            'users',
            [ 'filter': { 'is_author': true } ],
            {
                'count': 'count',
                'top10': [
                    [ 'sort', '-score' ],
                    [ 'page', 0, 10 ]
                ]
            }
        ]
    }

will return ``authors.count`` and ``authors.top10``.

Composable action groups::

    { 
        'authors': [
            'users',
            [ 'filter': { 'is_author': true } ],
            { 
                'male': [ 'filter', { 'gender': 'M' } ],
                'female': [ 'filter', { 'gender': 'F' } ]
            },
            {
                'count': 'count',
                'top10': [
                    [ 'sort', '-score' ],
                    [ 'page', 0, 10 ]
                ]
            }
        ]
    }

... will assess the third action group for each of the actions in the second action
group and thus return ``authors.male.count`` and ``authors.female.count`` and ``authors.male.top10`` and ``authors.female.top10``.
This may not prove to be all that useful.


Transport & Encoding
====================

By default the requests and responses are encoded as JSON and transported in the body of
HTTP POST requests::

    POST /api
    Content-Type: application/json
    Accept: application/json

    { 'user_count': [ 'users', 'count' ] }

HTTP response::

    200 OKAY
    Content-Type: application/json

    { 'user_count': 107 }

But this isn't the only option.
Transport could be by WebSockets or any of the message queue protocols.
XML / ProtoBuf / ASN1 encodings would be easy to define.


