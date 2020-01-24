from django.contrib.auth.backends import RemoteUserBackend
class RemoteUserCustomBackend(RemoteUserBackend):
    create_unknown_user = False

