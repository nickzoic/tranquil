class BaseContext(object):
    """all contexts inherit from this!"""

    def __init__(self, request):
        self.request = request

    def action(self, name, *params):
        if hasattr(self, 'action_' + name):
            getattr(self, 'action_' + name)(*params)
        raise NotImplementedError("action %s not found" % name)


class MultipleContext(BaseContext):

    def __init__(self, sub_contexts=None):
        self.sub_contexts = {}
        if sub_contexts:
            self.sub_contexts.update(sub_contexts)

    def action(self, name):
        return self.sub_contexts[name]
 
    def register(self, name):
        """Decorator to register a BaseContext subclass into this MultipleContext""" 
        def wrapper(cls):
            self.sub_contexts[name] = cls
            return cls
        return wrapper
        
