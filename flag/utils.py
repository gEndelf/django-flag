from datetime import date

from django.contrib.contenttypes.models import ContentType
from django.conf import settings


def get_content_type_tuple(content_type):
    """
    Return a tuple with `(app_name, model_name)` from "something"
    `content_type` can be :
     - a ContentType instance
     - a ContentType id (integer or stringified integer)
     - a model
     - an instance of a model
     - a `app_label.model_name` string
    """

    # check if integer, as integer or string => content_type id
    if isinstance(content_type, int) or (
            isinstance(content_type, basestring) and content_type.isdigit()):
        ctype = ContentType.objects.get_for_id(content_type)
        app_label, model = ctype.app_label, ctype.model

    # check if string => 'app_label.model_name'
    elif isinstance(content_type, basestring):
        try:
            app_label, model = content_type.split('.', 1)
        except Exception, e:
            raise e

    # check if its a content_type object
    elif isinstance(content_type, ContentType):
        app_label, model = content_type.app_label, content_type.model

    # check if a model (or an instance of a model)
    else:
        try:
            app_label = content_type._meta.app_label
            model = content_type._meta.model_name
        except Exception, e:
            raise e

    return app_label, model


def can_user_be_trusted(user):
    """
    This method is used to test if the given user meets the requirements to add a flag.
    for now, we only test the number of days the user has subscribed against FLAG_TRUST_TIME
    settings.FLAG_TRUST_TIME should be a number of days
    """
    return ((date.today() - user.date_joined.date()).days > settings.FLAG_TRUST_TIME)
