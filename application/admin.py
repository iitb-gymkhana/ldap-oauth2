from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Application


class ApplicationAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'name', 'user', 'total_users', 'created_on', 'modified_on', 'is_verified']
    list_filter = ['is_anonymous', 'is_verified']
    search_fields = ['name', 'user__username', 'user__first_name', ]
    raw_id_fields = ('user',)

    def total_users(self, obj):
        return obj.get_user_count()


admin.site.unregister(Application)
admin.site.register(Application, ApplicationAdmin)
