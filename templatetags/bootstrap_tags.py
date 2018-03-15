import re

from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


register = template.Library()

success_regex = re.compile(r"success", flags=re.I)
warning_regex = re.compile(r"(canceled)|(finished)", flags=re.I)
important_regex = re.compile(r"(failure)|(revoked)", flags=re.I)

help_dict = {
    'default':'Click here to read our training documents.',
    'acc_settings':'Click here for more information on account settings.',
    'cov_maps':'Click here for more information on coverage maps.',
    'map':'Click here for more information on using the map.',
    'upload_aoi':'Click here for more information on uploading an AOI.',
    'aoi_geocoords':'Click here for more information on creating an AOI from geo coordinates.',
    'aoi_subscribe':'Click here for more information on AOI subscriptions.',
    'export_pc':'Click here for more information on exporting pointcloud data.',
    'export_dem':'Click here for more information on creating DEMs from pointclouds.',
    'export_raster':'Click here for more information on exporting DEMs/imagery.',
    'bare_earth':'Click here for more information on using bare earth filters.',
    'hlz':'Click here for more information on generating HLZs.',
    'los':'Click here for more information on generating 3D LOS.',
    'slope':'Click here for more information on generating slopes.',
    'fete':'Click here for more information on generating FETE.',
    'plasio':'Click here for more information on using plas.io.',
    'new_wg':'Click here for more information on creating a new workgroup.',
    'manage_wg':'Click here for more information on managing workgroups.',
    'add_aoi_wg_new': 'Click here for more information on adding an AOI to a new workgroup.',
    'add_aoi_wg': 'Click here for more information on adding an AOI to an existing workgroup.'
}


@register.inclusion_tag("bootstrap_field.html")
def bootstrap_field(field, class_=None, label_tag=True, input_col_xs_size='col-6', _bold=False):
    input_ = field.as_widget(attrs={'class': class_ })
    id_for_label = field.id_for_label
    default_class = 'col-form-label col-2'
    field_class = default_class + " bold-label" if _bold else default_class
    label_tag = field.label_tag(attrs={'class': field_class})
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
    if taskstate:
        task_url = reverse('task_detail', args=(taskstate.task_id,))
        text = '<a href="{0}">{1}</a>'.format(task_url, text)
        if taskstate.is_cancelable():
            cancel_url = reverse('task_revoke_modal', args=(taskstate.task_id,))
            cancel_text = ('<span '
                           'class="fa fa-times" '
                           'aria-hidden="true"></span>')
            text += '&nbsp;<a class="btn btn-sm btn-default cancel-btn" onclick="cancelModal(\'{0}\');" href="#">{1}</a>'.format(cancel_url, cancel_text)
    return mark_safe(text)

@register.simple_tag
def help_icon(link="default"):
    training_url = reverse('training', args=(link,))
    help_text = help_dict[link]
    help_icon = ('<a href="{0}" target="_blank" '
        'data-toggle="tooltip" '
        'data-container="body" '
        'data-placement="right" '
        'data-original-title="{1}">'
        '<span class="far '
        'fa-question-circle '
        'help-gly" '
        'aria-hidden="true"></span>'
        '</a>').format(training_url, help_text)
    return mark_safe(help_icon)
