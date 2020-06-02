from django.contrib.auth import get_user_model
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.middleware import RemoteUserMiddleware
from account.models import UserProfile

class RemoteUserCustomMiddleware(RemoteUserMiddleware):
    def process_request(self, request):
        res = super(RemoteUserCustomMiddleware, self).process_request(request)

        # Configure from request
        def set_key(obj, key, valkey, valkey2):
            if valkey in request.META and getattr(obj, key) != request.META[valkey]:
                setattr(obj, key, request.META[valkey])
                set_key.changed = True

            if valkey2 in request.META and getattr(obj, key) != request.META[valkey2]:
                setattr(obj, key, request.META[valkey2])
                set_key.changed = True

        # Track changes
        set_key.changed = False

        # Update object
        user = request.user
        if request.user.is_authenticated:
            set_key(user, 'email', 'AUTHENTICATE_MAIL', 'OIDC_CLAIM_mail')
            set_key(user, 'first_name', 'AUTHENTICATE_GIVENNAME', 'OIDC_CLAIM_givenName')
            set_key(user, 'last_name', 'AUTHENTICATE_SN', 'OIDC_CLAIM_sn')

            if hasattr(request.user, 'userprofile'):
                profile = request.user.userprofile
            else:
                profile = UserProfile.objects.create(user=user)

            set_key(profile, 'roll_number', 'AUTHENTICATE_EMPLOYEENUMBER', 'OIDC_CLAIM_employeeNumber')
            set_key(profile, 'type', 'AUTHENTICATE_EMPLOYEETYPE', 'OIDC_CLAIM_employeeType')

            if set_key.changed:
                user.save()
                profile.save()

        return res

class RemoteUserCustomBackend(RemoteUserBackend):
    create_unknown_user = True

