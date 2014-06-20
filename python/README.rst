=====================
 Tranquil for Python
=====================


Files under ``python`` are an installable python package which will eventually
get uploaded to PyPI.

``tranquil.contexts.BaseContext`` provides a base for generic context
objects in Python.  Each backend context inherits from this.


Django
======

``tranquil.django.contexts.DjangoModelContext`` provides a simple set of
actions which map onto the Django database API.  There's some example code
under ``python/examples/django/``

This is an implementation of a Tranquil API over Django.
The installable module is under 'tranquil' and an example Django project
and app are under 'examples/django'.

To actually use this code, subclass DjangoModelContext into your own model
contexts and override methods as appropriate to implement your business rules.


TODO
====

* DjangoModelWithPermissionsContext: subclass DjangoModelContext to enforce
  permissions as per django.contrib.auth's Permission system.


