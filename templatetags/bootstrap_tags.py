import re

from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

register = template.Library()

success_regex = re.compile(r"success", flags=re.I)
warning_regex = re.compile(r"(cancelled)|(finished)", flags=re.I)
important_regex = re.compile(r"(failure)|(revoked)", flags=re.I)


@register.inclusion_tag("bootstrap_field.html")
def bootstrap_field(field, class_=None, label_tag=True, input_col_xs_size='col-xs-6'):
    input_ = field.as_widget(attrs={'class': class_ })
    id_for_label = field.id_for_label
    label_tag = field.label_tag(attrs={'class': 'control-label col-xs-2'}) if not field.is_hidden and label_tag else ''
    help_text = field.help_text
    wrapper_class = 'has-error' if field.errors else ''
    input_col_xs_size = input_col_xs_size
    errors = ' '.join(field.errors)
    return {'label': label_tag, 'input': input_, 'help_text': help_text,
            'wrapper_class': wrapper_class, 'errors': errors,
            'hidden': field.is_hidden, 'id_for_label': id_for_label,
            'input_col_xs_size': input_col_xs_size,
            'use_tooltips': settings.BOOTSTRAP_TOOLTIPS}


@register.filter
def form_verb(obj):
    return "Update" if obj else "Add"

@register.filter
def alt_form_verb(obj):
    return "Edit" if obj else "Create"


@register.simple_tag
def label(text, taskstate=None):
    try:
        text_for_class = taskstate.state
    except AttributeError:
        text_for_class = text
    label_class = ''
    if success_regex.match(text_for_class):
        label_class = "alert-success"
    elif warning_regex.match(text_for_class):
        label_class = "alert-warning"
    elif important_regex.match(text_for_class):
        label_class = "alert-danger"
    else:
        label_class = "alert-info"
    text = '<span class="badge %s">%s</span>' % (label_class, text)
    return text


@register.simple_tag
def label_link(taskstate, user, custom_state=None):
    if custom_state is not None:
        state = custom_state
    elif taskstate is not None:
        try:
            state = taskstate.state
        except AttributeError:
            state = taskstate
    else:
        state = 'UNKNOWN'
    text = label(state, taskstate)
    if taskstate and user.has_module_perms('taskstate'):
        url = reverse('task_detail', args=(taskstate.task_id,))
        text = '<a href="%s">%s</a>' % (url, text)
    return text
