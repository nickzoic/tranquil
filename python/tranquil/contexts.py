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

    def process(self, actions):
        """Handle the complexities of the Action/ActionList/ActionGroup
        data structure by recursing down into it."""
        
        # XXX should this really be in this class anyway?
        # XXX should we iterate where possible instead of recursing?

        if type(actions) is list:
            # actions is an Action List
            action = actions.pop(0)
            if type(action) in (str, unicode): action = [ action ]
            new = self.action(*action)
            if actions: new = new.process(actions)
            return new

        elif type(actions) is dict:
            # actions is an Action Group
            return dict([
                (label, self.process(sub_actions))
                for label, sub_actions in actions.items()
            ])

        elif type(actions) in (str, unicode):
            # actions is a shortcut for a single Action
            return self.action(actions)

        else:
            raise NotImplementedError('bad actions')

