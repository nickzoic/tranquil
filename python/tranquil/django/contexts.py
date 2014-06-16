from tranquil.contexts import BaseContext
from django.core import serializers

import json


class DjangoModelContext(BaseContext):
    """Generic Context for a Django Model class"""
    model=None

    def __init__(self, request, queryset=None):
	assert self.model, "DjangoModelContext subclasses must specify 'model'"
        self.request = request
        self.queryset = queryset or self.model.objects.all()

    def action_filter(self, filter_dict):
	"""Filter operation, takes a kwargs dictionary sent to Django's filter.
	See https://docs.djangoproject.com/en/dev/ref/models/querysets/#filter"""
        return self.__class__(self, self.queryset.filter(**filter_dict))

    def action_order_by(self, *order_by):
	"""Sorts the context result
	See https://docs.djangoproject.com/en/dev/ref/models/querysets/#order-by"""
        return self.__class__(self, self.queryset.order_by(order_by))

    def action_count(self):
	"""Returns only a count of items matched by this context.
	See https://docs.djangoproject.com/en/dev/ref/models/querysets/#count"""
        return self.queryset.count()

    def action_update(self, fields_dict):
	"""Updates all items matched by this context.  Takes a dictionary of
	attributes to update.
	See https://docs.djangoproject.com/en/dev/ref/models/querysets/#update"""
	self.queryset.update(**fields_dict)
	return self

    def action_delete(self):
	"""Bulk delete of items matched by this context.
	See https://docs.djangoproject.com/en/dev/ref/models/querysets/#delete"""
	self.queryset.delete()
	return None

    def action_meta(self):
	"""Returns metadata on this context and the available actions."""
	return {
	    "desc": self.__class__.__doc__,
	    "class": self.__class__.__name__,
	    "model": self.model.__class__.__name__,
	    "actions": dict([
	        (method_name[7:], { "desc": getattr(self, method_name).__doc__ })
	        for method_name in dir(self)
	        if method_name.startswith("action_")
	    ])
	}

    def serialize(self):
	# XXX AWFUL HACK ... this obviously needs to be improved a lot
	# to handle weirder cases, recursion, etc.
	# Can probably get a good start from
	# django.core.serializers.python.Serializer

        return [
            dict([('id', x['pk'])] + x['fields'].items())
            for x in json.loads(serializers.serialize("json", self.queryset))
        ]

