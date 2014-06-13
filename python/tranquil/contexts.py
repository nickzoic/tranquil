class BaseContext(object):
    """all contexts inherit from this!"""

    def __init__(self, request):
        self.request = request

    def action(self, name, *params):
        """Despatches actions off to action_* methods, which should
        return either a context or some data"""

        action_method_name = 'action_%s' % name
        if hasattr(self, action_method_name):
            return getattr(self, action_method_name)(*params)
        raise NotImplementedError("action %s not found in %s.%s" % (name, self.__class__.__name__, action_method_name))
