from django import get_version
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.utils.translation import string_concat

from flag.models import FlaggedContent, FlagInstance
from django import forms
from django.contrib.admin import SimpleListFilter
from flag import settings as flag_settings


class FlagInstanceFormSet(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(FlagInstanceFormSet, self)._construct_form(i, **kwargs)
        content_object = form.instance.flagged_content.content_object
        choices = flag_settings.get_for_model(content_object, 'STATUSES')
        form.fields['status'] = forms.ChoiceField(label="Status",
                                                  choices=choices)
        return form


class InlineFlagInstance(admin.TabularInline):
    formset = FlagInstanceFormSet
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


class StatusFilter(SimpleListFilter):
    title = 'status' # or use _('country') for translated title
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        model_settings = flag_settings.MODELS_SETTINGS
        statuses = set([s.status for s in model_admin.model.objects.all()])
        filters = []

        def get_from_choices(choices):
            for choice in choices:
                if status == choice[0]:
                    labels.append(choice[1])

        for status in statuses:
            labels = []
            get_from_choices(flag_settings.STATUSES)

            for model_name in model_settings:
                model = model_settings[model_name]
                if 'STATUSES' in model:
                    get_from_choices(model['STATUSES'])
            if labels:
                label = labels[0]
                if len(labels) > 1:
                    for _label in labels[1:]:
                        label = string_concat(label, u' | ', _label)
            else:
                label = status
            filters.append((status, label))
        return filters

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        else:
            return queryset


class FlaggedContentAdmin(admin.ModelAdmin):
    form = FlaggedContentForm
    inlines = [InlineFlagInstance]
    list_display = ('id', '__unicode__', 'get_status', 'count')
    list_display_links = ('id', '__unicode__')
    list_filter = (StatusFilter,)
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
