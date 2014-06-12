from tranquil.contexts import BaseContext


class DjangoModelContext(BaseContext):
    # model is set up by the subclasses

    def __init__(self, request, context):
        self.request = request
        self.queryset = model.objects.all()

    def action_filter(self, name, filter_dict):
        self.queryset = context.queryset.filter(**filter_dict)

    def action_order_by(self, name, *order_by):
        self.queryset = context.queryset.order_by(order_by)

    def action_count(self, name):
        self.result = context.queryset.count()


