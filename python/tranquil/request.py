# XXX not actually used at the moment

from tranquil.contexts import BaseContext


def process_action_list(action_list, context_class):

    new_context = context_class()
    for action in action_list:
        new_context = new_context.action(*action)
    if isinstance(BaseContext, new_context):
        return new_context.serialize()
    else:
        return new_context


def process_action_group(action_group, context_class):

    return dict([
        (action_label, process_request(action, context_class))
        for action_label, action in action_group.items():
    ])


def process_request(action_data, context_class):

    if type(action_data) is dict:
        process_action_group(action_data, context_class)
    elif type(action_data) is list:
        process_action_list(action_data, context_class)
    elif type(action_data) in (str, unicode):
        process_action_list([[action_data]], context_class)
    else:
        raise NotImplementedError()
         
