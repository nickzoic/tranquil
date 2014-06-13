==========
 TRANQUIL
==========
----------------------------
 Nick Moore <nick@zoic.org> 
----------------------------

Tranquil is a protocol framework which helps define the way that a client 
connects to a server.  It is designed to be very simple and very extensible.

In terms of complexity, it fits somewhere between
`REST <http://en.wikipedia.org/wiki/Representational_state_transfer>`_
and `SOAPjr <http://www.soapjr.org/>`_.


Querying
========


Context
-------

A *context* describes a group of resources.
For example, a context could be "all users" or "all active users"
or "all users over 35".

A context is specific to a request, so it knows who is asking and
can enforce business rules.  For example, a context for an unauthorized
user may retrieve fewer fields from the user object that the context
for an administrator user.


Actions
-------

*Actions* transform contexts into other contexts
**OR** into data which is returned in the response.
For example, the "all users" context could be transformed into 
the "users over 35" context using a "filter" action.

Not all actions return a new context: some may produce
data for return to the client.

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

However, if the righthand side is a list it **MUST** be an action list,
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

Typically, requests are encoded as JSON and transported in the body of
HTTP POST requests::

    POST /api
    Content-Type: application/json
    Accept: application/json

    { "user_count": [ "users", "count" ] }

The request body is interpreted as a JSON data structure and treated
as an action list if an array or as an action group if an object.

The HTTP response also contains JSON::

    200 OK
    Content-Type: application/json

    { "user_count": 107 }

In the case of JSON or Tranquil syntax errors, HTTP status
``400 Bad Request`` is returned.  Other error codes may be returned
for other issues.


Using from vanilla javascript
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A very simple example which doesn't need any external libraries or 
frameworks (but has no error handling)::

    function tranquil_request(url, request, callback) {
        var xhr = new XMLHttpRequest();
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                var response = JSON.parse(xhr.response);
                callback(response);
            }
        };
        xhr.open('POST', url, true);
        xhr.send(JSON.stringify(request));
    }
    
    tranquil_request('/api', { user_count: [ "users", "count" ] }, function (response) {
        alert(response.user_count);
    });
    
    
Using from jQuery
~~~~~~~~~~~~~~~~~

Using `jQuery's AJAX function <http://api.jquery.com/jQuery.ajax/>`_::

    var request = {
        user_count: [ "users", "count" ]
    };
    
    $.ajax({
        type: "POST",
        url: "/api",
        processData: false,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(request)
    }).done(function (response, jqxhr) {
        alert(jqxhr.responseJSON.user_count);        
    });


Other Encodings
---------------

The above examples are all in JSON, but 
`ProtoBuf <https://code.google.com/p/protobuf/>`_ /
`XML <http://www.w3.org/XML/>`_ /
`ASN1 <http://en.wikipedia.org/wiki/Abstract_Syntax_Notation_One>`_ /
`S-expression <http://rosettacode.org/wiki/S-Expressions>`_
encodings would be easy to define 
if there was a need to do so.

Implementations using HTTP transport
should use the HTTP ``Content-Type`` and ``Accept`` headers to decide
which encoding is appropriate for requests and responses.


Other Transports
----------------

Tranquil is transport-agnostic, so transport could be by 
`WebSockets <http://websocket.org/>`_, `AMQP <http://amqp.org/>`_
or `avian carrier <http://www.ietf.org/rfc/rfc1149.txt>`_.

The same resources can be made available over multiple transports 
to allow for backwards compatibility.


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

**In progress ...**


Django
------

`Django <http://djangoproject.com/`_ support includes a
``DjangoModelContext`` class which automatically makes available a 
large part of the
`Django query API <https://docs.djangoproject.com/en/1.6/topics/db/queries/`_
for access to your models.