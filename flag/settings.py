from django import conf
from django.utils.translation import ugettext_lazy as _

from flag.utils import get_content_type_tuple

__all__ = ('ALLOW_COMMENTS',
           'LIMIT_SAME_OBJECT_FOR_USER',
           'LIMIT_FOR_OBJECT',
           'MODELS',
           'STATUSES',
           'DEFAULT_STATUS',
           'SEND_MAILS',
           'SEND_MAILS_TO',
           'SEND_MAILS_FROM',
           'SEND_MAILS_RULES',
           'NEEDS_TRUST',
           'TRUST_TIME')

# keep the default values
_DEFAULTS = dict(
    ALLOW_COMMENTS=True,
    NEEDS_TRUST=False,
    TRUST_TIME=3,
    LIMIT_SAME_OBJECT_FOR_USER=0,
    LIMIT_FOR_OBJECT=0,
    MODELS=None,
    STATUSES=[
        (1, _("flagged")),
        (2, _("flag rejected by moderator")),
        (3, _("creator notified")),
        (4, _("content removed by creator")),
        (5, _("content removed by moderator")),
    ],
    DEFAULT_STATUS=1,
    SEND_MAILS=False,
    SEND_MAILS_TO=conf.settings.ADMINS,
    SEND_MAILS_FROM=conf.settings.DEFAULT_FROM_EMAIL,
    SEND_MAILS_RULES=[(1, 1), ],
    MODELS_SETTINGS={},
)

# Set FLAG_ALLOW_COMMENTS to False in settings to not allow users to
# comment their flags (True by default)
ALLOW_COMMENTS = getattr(conf.settings,
                         'FLAG_ALLOW_COMMENTS',
                         _DEFAULTS['ALLOW_COMMENTS'])

# boolean stating whether an user needs to be trusted before being
# able to flag some content
NEEDS_TRUST = getattr(conf.settings, 
                     'FLAG_NEEDS_TRUST',
                     _DEFAULTS['NEEDS_TRUST'])
# The number of days that a user must have created his account 
# before he is allowed to flag content
TRUST_TIME = getattr(conf.settings, 
                     'FLAG_TRUST_TIME',
                     _DEFAULTS['TRUST_TIME'])

# Set FLAG_LIMIT_SAME_OBJECT_FOR_USER to a number in settings to limit the
# times a user can flag a single object
# If 0, there is no limit
LIMIT_SAME_OBJECT_FOR_USER = getattr(conf.settings,
                                     'FLAG_LIMIT_SAME_OBJECT_FOR_USER',
                                     _DEFAULTS['LIMIT_SAME_OBJECT_FOR_USER'])

# Set FLAG_LIMIT_FOR_OBJECT to a number in settings to limit the times an
# object can be flagged
# If 0, there is no limit
LIMIT_FOR_OBJECT = getattr(conf.settings,
                           'FLAG_LIMIT_FOR_OBJECT',
                           _DEFAULTS['LIMIT_FOR_OBJECT'])

# Set FLAG_MODELS to a list/tuple of models in your settings to limit the
# models that can be flagged. The syntax to use is a string for each model :
# FLAG_MODELS = ('myapp.mymodel', 'otherapp.othermodel',)
MODELS = getattr(conf.settings, 'FLAG_MODELS', _DEFAULTS['MODELS'])

# Set FLAG_STATUSES to a list of tuples in your settings to set the available
# status for each flagged content
# The default status used when a user flag an object is the first of this list.
STATUSES = getattr(conf.settings, "FLAG_STATUSES",
            getattr(conf.settings, "FLAG_STATUS", _DEFAULTS['STATUSES']))

# Set FLAG_DEFAULT_STATUS to ... the default status
DEFAULT_STATUS = getattr(conf.settings, 'FLAG_DEFAULT_STATUS', 
                         _DEFAULTS['DEFAULT_STATUS'])

# Set FLAG_SEND_MAILS to True if you want to have emails sent when object are
# flagged.
# See others settings FLAG_SEND_MAILS_* for more configuration
# The default is to not send mails
SEND_MAILS = getattr(conf.settings, "FLAG_SEND_MAILS", _DEFAULTS['SEND_MAILS'])

# Set FLAG_SEMD_MAILS_TO to a list of email addresses to sent mails when an
# object is flagged.
# Each entry can be either a single email address, or a tuple with (name, email
# address) but only the mail will be used
# The default is the ADMINS setting
SEND_MAILS_TO = getattr(conf.settings,
                        "FLAG_SEND_MAILS_TO",
                        _DEFAULTS['SEND_MAILS_TO'])

# Set FLAG_SEND_MAILS_FROM to an email address to use as the send of mails
# sent when an object is flagged.
# Default to the DEFAULT_FROM_EMAIL setting
SEND_MAILS_FROM = getattr(conf.settings,
                          "FLAG_SEND_MAILS_FROM",
                          _DEFAULTS['SEND_MAILS_FROM'])

# Set FLAG_SEND_MAILS_RULES to define when to send mails for flags. This
# settings is a list of tuple, each line defining a rule. A rule is a tuple
# with two entries, the first one is the minimum flag for an object for which
# this rule apply, and the second one is the frequency : (4, 3) => if an
# object is flagged 4 times or more, send a mail every 3 flags (4, 7 and 10).
# If this rule is followed by (10, 5), it will be used only when number of
# flags is between 4 (included) and 10 (not included), then the "11" rules
# will apply.
# A mail will be send if the LIMIT_FOR_OBJECT is reached, ignoring the rules
# Default is to sent a mail for each flag
SEND_MAILS_RULES = getattr(conf.settings,
                           "FLAG_SEND_MAILS_RULES",
                           _DEFAULTS['SEND_MAILS_RULES'])

# Use FLAG_MODELS_SETTINGS if you want to override the global settings for a
# specific model.
# It's a dict with the string represetation of the model (`myapp.mymodel`) as
# key, and a dict as value. This last dict can have zero, one or more of the
# settings described in this module (excepted `MODELS` and of course
# `MODELS_SETTINGS`), using names WITHOUT the `FLAG_` prefix
# Default to an empty dict : each model will use the global settings
MODELS_SETTINGS = getattr(conf.settings,
                          "FLAG_MODELS_SETTINGS",
                          _DEFAULTS['MODELS_SETTINGS'])

# do not send mails if no recipients
if SEND_MAILS and not SEND_MAILS_TO:
    SEND_MAILS = False

_ONLY_GLOBAL_SETTINGS = ('MODELS', 'MODELS_SETTINGS',)


def get_for_model(model, name):
    """
    Try to get the `name` settings for a specific model.
    See `utils.get_content_type_tuple` for description of the `name` parameter
    The fallback in all case (all exceptions or simply no specific
    settings) is the basic settings
    """
    from flag import settings as flag_settings
    result = getattr(flag_settings, name)
    if name not in _ONLY_GLOBAL_SETTINGS:
        try:
            model_id = '%s.%s' % get_content_type_tuple(model)
        except:
            pass
        else:
            if name in MODELS_SETTINGS.get(model_id, {}):
                result = MODELS_SETTINGS[model_id][name]
    return result
