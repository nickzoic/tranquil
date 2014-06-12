from tranquil.contexts import BaseContext
from django.core import serializers
import json

class DjangoModelContext(BaseContext):
    # model is set up by the subclasses

    def __init__(self, parent_context, queryset=None):
        self.request = parent_context.request
        self.queryset = queryset or self.model.objects.all()

    def action_filter(self, name, filter_dict):
        return self.__class__(self, self.queryset.filter(**filter_dict))

    def action_order_by(self, name, *order_by):
        return self.__class__(self, self.queryset.order_by(order_by)

    def action_count(self, name):
        return self.queryset.count()

    def serialize(self):
        return serializers.serialize("json", self.queryset)

