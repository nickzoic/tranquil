from tranquil.contexts import BaseContext


def process_action_list(action_list, context):

    new = context
    for action in action_list:
        if type(action) is dict:
            new = process_action_group(action, new)
        elif type(action) is list:
            new = new.action(*action)
        else:
            new = new.action(action)

    if isinstance(new, BaseContext):
        return new.serialize()
    else:
        return new


def process_action_group(action_group, context):

    return dict([
        (label, process_request(action, context))
        for label, action in action_group.items()
    ])


def process_request(actions, context):

    if type(actions) is dict:
        return process_action_group(actions, context)

    elif type(actions) is list:
        return process_action_list(actions, context)

    elif type(actions) in (str, unicode):
        process_action_list([[actions]], context)

    else:
        raise NotImplementedError()

