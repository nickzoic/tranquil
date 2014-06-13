from tranquil.contexts import BaseContext
from django.core import serializers

import json


class DjangoModelContext(BaseContext):
    # model is set up by the subclasses

    def __init__(self, request, queryset=None):
        self.request = request
        self.queryset = queryset or self.model.objects.all()

    def action_filter(self, filter_dict):
        return self.__class__(self, self.queryset.filter(**filter_dict))

    def action_order_by(self, *order_by):
        return self.__class__(self, self.queryset.order_by(order_by))

    def action_count(self):
        return self.queryset.count()

    def action_update(self, fields_dict):
	self.queryset.update(**fields_dict)
	return self

    def action_delete(self):
	self.queryset.delete()
	return None

    def serialize(self):
	# XXX AWFUL HACK ... this obviously needs to be improved a lot
	# to handle weirder cases, recursion, etc.
	# Can probably get a good start from
	# django.core.serializers.python.Serializer

        return [
            dict([('id', x['pk'])] + x['fields'].items())
            for x in json.loads(serializers.serialize("json", self.queryset))
        ]

