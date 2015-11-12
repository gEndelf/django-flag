from django import template

from flag.forms import get_default_form
from flag.views import get_next, get_confirm_url_for_object, can_be_flagged_by
from flag.models import FlaggedContent

register = template.Library()


@register.inclusion_tag("flag/flag_form.html", takes_context=True)
def flag(context, content_object, creator_field=None, with_status=False):
    """
    This templatetag will display a form to flag the given object.
    If the `creator_field` is given, the field will be added to the form in
    an hidden input.
    If the `with_status` is True, a `status` will be added
    """
    if not content_object:
        return {}
    request = context.get('request', None)
    form = get_default_form(content_object, creator_field, with_status)
    return dict(form=form,
                next=get_next(request))


@register.inclusion_tag("flag/flag_form.html", takes_context=True)
def flag_with_status(context, content_object, creator_field=None):
    """
    Helper for the `flag` templatetag, which set `with_status` to True
    """
    return flag(context, content_object, creator_field, True)


@register.filter
def flag_count(content_object):
    """
    This filter will return the number of flags for the given object
    Usage : {{ some_object|flag_count }}
    """
    try:
        return FlaggedContent.objects.get_for_object(content_object).count
    except:
        return 0


@register.filter
def flag_status(content_object, full=False):
    """
    This filter will return the flag's status for the given object
    Usage : {{ some_object|flag_status }}
    If `full` is True, the text of the status will be displayed.
    Usage : {{ some_object|flag_status:"text" }}
    """
    try:
        flagged_content = FlaggedContent.objects.get_for_object(content_object)
        if full:
            return flagged_content.get_status_display()
        return flagged_content.status
    except:
        return None

register.filter(can_be_flagged_by)


@register.filter
def flag_confirm_url(content_object, creator_field=None):
    """
    This filter will return the url of the flag confirm page for the given
    object
    Usage: {{ some_object|flag_confirm_url }}
    Or, with a creator_field : {{ some_object|flag_confirm_url:"some_field" }}
    """
    try:
        return get_confirm_url_for_object(content_object, creator_field, False)
    except:
        return ""


@register.filter
def flag_confirm_url_with_status(content_object, creator_field=None):
    """
    This filter will return the url of the flag confirm page for the given
    object.
    The difference with `flag_confirm_url` is that in this form the user will
    ne able to choose the flag's status
    Usage: {{ some_object|flag_confirm_url_with_status }}
    Or, with a creator_field :
        {{ some_object|flag_confirm_url_with_status:"some_field" }}
    """
    try:
        return get_confirm_url_for_object(content_object, creator_field, True)
    except:
        return ""
