class BaseContext(object):
    """all contexts inherit from this!"""

    def __init__(self, request):
        self.request = request

    def action(self, name, *params):
        action_method_name = 'action_%s' % name
        if hasattr(self, action_method_name):
            return getattr(self, action_method_name)(*params)
        raise NotImplementedError("action %s not found" % name)

    def process(self, actions):
        """Handle the complexities of the Action/ActionList/ActionGroup
        data structure by recursing down into it."""
        
        # XXX should this really be in this class anyway?
        # XXX should we iterate where possible instead of recursing?

        if type(actions) is list:
            # actions is an Action List
            action = actions.pop()
            if type(action) in (str, unicode): action = [ action ]
            new = self.action(*action)
            if actions: new = new.process(actions)
            return new

        elif type(actions) is dict:
            # actions is an Action Group
            return dict([
                (label, self.action(sub_actions))
                for label, sub_actions in actions
            ])

        elif type(actions) in (str, unicode):
            # actions is a shortcut for a single Action
            return self.action(actions)

        else:
            raise NotImplementedError('bad actions')


# XXX Don't think this was very well thought out ...
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
        
