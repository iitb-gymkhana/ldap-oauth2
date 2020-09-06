import pprint

from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
from simple_history.admin import SimpleHistoryAdmin

from .models import Application


class ApplicationAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'name', 'user', 'total_users', 'created_on', 'modified_on', 'is_verified', 'is_beta']
    list_filter = ['is_anonymous', 'is_verified', 'is_beta']
    search_fields = ['name', 'user__username', 'user__first_name', ]
    raw_id_fields = ('user',)

    def total_users(self, obj):
        return obj.get_user_count()

    def save_model(self, request, obj, form, change):
        messages = []

        if 'is_verified' in form.changed_data:
            messages.append('Client verified set to ' + str(form.cleaned_data['is_verified']))
        if 'is_beta' in form.changed_data:
            messages.append('Client public beta set to ' + str(form.cleaned_data['is_beta']))

        if len(messages) > 0:
            secret = form.cleaned_data['client_secret']
            form.cleaned_data['client_secret'] = '***'
            form.cleaned_data['creator'] = str(form.cleaned_data['user'])

            html = '<h3> Action in Gymkhana Profiles by ' + str(request.user) + ' on ' + obj.name + '</h3>'
            for m in messages:
                html += '<h4>' + m + '</h4>'
            html += '<br><h4>Client information</h4>'
            html += '<pre>' + pprint.pformat(form.cleaned_data) + '</pre>'

            form.cleaned_data['client_secret'] = secret
            del form.cleaned_data['creator']

            send_mail(
                settings.EMAIL_SUBJECT_PREFIX + ' Change to client ' + obj.name,
                html, None, settings.VERIFIED_NOTIF_EMAILS,
                html_message=html,
                fail_silently=False,
            )

        return super().save_model(request, obj, form, change)


admin.site.unregister(Application)
admin.site.register(Application, ApplicationAdmin)
