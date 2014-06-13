==========
 TRANQUIL
==========


Querying
========


Context
-------

A *context* describes a group of resources.
For example, a context could be "all users" or "all active users"
or "all users over 35".

A context is specific to a request, so it knows who is asking and
can enforce business rules.


Actions
-------

*Actions* transform contexts into other contexts
*OR* into data which is returned in the response.
For example, the "all users" context could be transformed into 
the "users over 35" context using a "filter" action.

Not all actions return a new context: some may 
return data for serialization.  

An action is represented as a list of an *action_name*
and some *parameters*.  Parameters can be any data type,
and there may be multiple of them.

*As a shortcut, actions without parameters can be represented
as plain strings.*

Example actions::

    "count"

    [ "count" ]

    [ "before", "2011-12-13" ]

    [ "between", 7, 12 ]

    [ "colors", [ "red", "green", "blue" ] ]

    [ "filter", { "is_active": true } ]

Action names are expected to be strings matching
``[A-Za-z0-9][A-Za-z0-9_]*`` although this may be expanded later.


Action Lists
------------

An *action list* is a list of actions, which compose left to right.

Example action_lists::

    [ "count" ]

    [ [ "filter", { "is_author": true } ], "count" ]

In the second example, the initial context is first filtered
to make a new context, then the number of records in the context
are counted and the count is returned.


Action Groups
-------------

An *action group* labels actions and runs them in parallel in the
same context.
The structure is ``{ action_label: action_list }``.

*As a shortcut, if the righthand side is a plain string it is assumed
to be the name of a single action with no parameters.*

However, if the righthand side is a list it *MUST* be an action list,
not an individual action.  A single action must be wrapped into an 
action list to avoid syntactic confusion::

    {
        "count": "count",
        "page": [ [ "page", 0, 5 ] ]
    }

The *action labels* are a convenience to the frontend programmer:
they are used to construct a response.  For example, the above
query returns something like::

    {
         "count": 107,
         "page": [ {...}, {...}, {...}, {...}, {...} ]
    }

... this is done for readability and so so that you can
conveniently refer to ``response.count`` and ``response.page[n]``
from javascript.


Nesting Action Groups
~~~~~~~~~~~~~~~~~~~~~

Action groups nest::

    { 
        "authors": [
            "users",
            [ "filter": { "is_author": true } ],
            {
                "count": "count",
                "top10": [
                    [ "sort", "-score" ],
                    [ "page", 0, 10 ]
                ]
            }
        ]
    }

will return ``authors.count`` and ``authors.top10``.


Composing Action Groups
~~~~~~~~~~~~~~~~~~~~~~~

Composable action groups::

    { 
        "authors": [
            "users",
            [ "filter": { "is_author": true } ],
            { 
                "male": [ "filter", { "gender": "M" } ],
                "female": [ "filter", { "gender": "F" } ]
            },
            {
                "count": "count",
                "top10": [
                    [ "sort", "-score" ],
                    [ "page", 0, 10 ]
                ]
            }
        ]
    }

... will assess the third action group for each of the actions
in the second action group and thus return
``authors.male.count`` and ``authors.female.count`` and
``authors.male.top10`` and ``authors.female.top10``.

*This may not prove to be all that useful and implementations may
choose to not support it.*


Writing with Actions
--------------------

The examples above are all read-only actions.  Actions may also 
mutate database state.  Operations apply to all resources in the 
current context::

    [
        "users",
        [ "filter": { "age": [ "gt", "40" ] } ],
        [ "update": { "trust": false } ]
    ]

Mutating actions aren't limited to Create, Update and Delete.
For example, actions could be defined for Increment, Append,
Shuffle, Swap.


Transport & Encoding
====================


HTTP POST and JSON
------------------

Requests and responses are encoded as JSON and transported in the body of
HTTP POST requests::

    POST /api
    Content-Type: application/json
    Accept: application/json

    { "user_count": [ "users", "count" ] }

The request body is interpreted as a JSON data structure and treated
as an action list if an array or as an action group if an object.

HTTP response::

    200 OKAY
    Content-Type: application/json

    { "user_count": 107 }

In the case of JSON or Tranquil syntax errors, HTTP status
``400 BAD REQUEST`` is returned.  Other error codes may be returned
for other issues.


Other Encodings
---------------

ProtoBuf / XML / ASN1 / S-expression encodings would be easy to define 
if there was a need to do so.  Implementations using HTTP transport
should use the HTTP ``Content-Type`` and ``Accept`` headers to decide
which encoding is appropriate.


Other Transports
----------------

Tranquil is transport-agnostic, so transport could be by WebSockets,
AMPQ or avian carrier.


Transactions
============

Where possible, the whole query should be handled in a single
transaction, which should be rolled back if any part fails.  As 
a Tranquil API can run on non-Transactional stores, or across 
multiple stores, this may not always be possible.

Where nested transactions are available, each action list which 
contains a mutating action should have its own transaction, so
that the results of the mutation are visible from subsequent actions
in that action list but not from other action lists.


Implementation
==============


