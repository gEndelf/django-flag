from django import get_version
from django.contrib import admin

from flag.models import FlaggedContent, FlagInstance
from django import forms
from flag import settings as flag_settings


class FlagInstanceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FlagInstanceForm, self).__init__(*args, **kwargs)
        # TODO add choices for status field

    class Meta:
        model = FlagInstance
        fields = '__all__'


class InlineFlagInstance(admin.TabularInline):
    form = FlagInstanceForm
    model = FlagInstance
    extra = 0
    raw_id_fields = ('user', )


class FlaggedContentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FlaggedContentForm, self).__init__(*args, **kwargs)
        content_object = self.instance.content_object
        if content_object is not None:
            choices = flag_settings.get_for_model(content_object, 'STATUSES')
            self.fields['status'] = forms.ChoiceField(label="Status",
                                                      choices=choices)

    class Meta:
        model = FlaggedContent
        fields = '__all__'


class FlaggedContentAdmin(admin.ModelAdmin):
    form = FlaggedContentForm
    inlines = [InlineFlagInstance]
    list_display = ('id', '__unicode__', 'get_status', 'count')
    list_display_links = ('id', '__unicode__')
    list_filter = ('status',)
    readonly_fields = ('content_type', 'object_id')
    raw_id_fields = ('creator', 'moderator')
    if get_version() >= '1.4':
        fields = (('content_type', 'object_id'),
                  'creator',
                  'status',
                  'count',
                  'moderator')
    else:
        fields = ('content_type',
                  'object_id',
                  'creator',
                  'status',
                  'count',
                  'moderator')

    def get_status(self, obj):
        return obj.get_status_display()

    get_status.short_description = 'Status'


admin.site.register(FlaggedContent, FlaggedContentAdmin)
