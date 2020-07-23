from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import ContactNumber, InstituteAddress, Program, SecondaryEmail, SentMessage


class InstituteAddressAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'hostel', 'room']
    list_filter = ['hostel']
    search_fields = ['user__username', 'user__first_name', 'room']
    raw_id_fields = ('user',)


class ProgramAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'department', 'join_year', 'graduation_year', 'degree']
    list_filter = ['department', 'join_year', 'graduation_year', 'degree', ]
    search_fields = ['user__username', 'user__first_name', ]
    raw_id_fields = ('user',)

    class Media:
        js = ['admin/js/list_filter_collapse.js', ]


class ContactNumberAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'number']
    search_fields = ['user__username', 'user__first_name', 'number', ]
    raw_id_fields = ('user',)


class SecondaryEmailAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'email']
    search_fields = ['user__username', 'user__first_name', 'email', ]
    raw_id_fields = ('user',)


class SentMessageAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'message_id', 'sender', 'user', 'status', 'created', ]
    list_filter = ['status', 'sender', ]
    search_fields = ['sender__id', 'sender__name', 'user__username', 'user__first_name', 'message_id', ]
    raw_id_fields = ('user','sender')

    class Media:
        js = ['admin/js/list_filter_collapse.js', ]


admin.site.register(InstituteAddress, InstituteAddressAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(ContactNumber, ContactNumberAdmin)
admin.site.register(SecondaryEmail, SecondaryEmailAdmin)
admin.site.register(SentMessage, SentMessageAdmin)
