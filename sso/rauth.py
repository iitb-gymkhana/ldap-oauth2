from django.contrib.auth import get_user_model
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.middleware import RemoteUserMiddleware
from account.models import UserProfile

class RemoteUserCustomMiddleware(RemoteUserMiddleware):
    def process_request(self, request):
        res = super(RemoteUserCustomMiddleware, self).process_request(request)

        # Configure from request
        def set_key(obj, key, valkey):
            if valkey in request.META and getattr(obj, key) != request.META[valkey]:
                setattr(obj, key, request.META[valkey])
                set_key.changed = True

        # Track changes
        set_key.changed = False

        # Update object
        user = request.user
        if request.user.is_authenticated:
            set_key(user, 'email', 'AUTHENTICATE_MAIL')
            set_key(user, 'first_name', 'AUTHENTICATE_GIVENNAME')
            set_key(user, 'last_name', 'AUTHENTICATE_SN')

            if hasattr(request.user, 'userprofile'):
                profile = request.user.userprofile
            else:
                profile = UserProfile.objects.create(user=user)

            set_key(profile, 'roll_number', 'AUTHENTICATE_EMPLOYEENUMBER')
            set_key(profile, 'type', 'AUTHENTICATE_EMPLOYEETYPE')

            if set_key.changed:
                user.save()
                profile.save()

        return res

class RemoteUserCustomBackend(RemoteUserBackend):
    create_unknown_user = True

