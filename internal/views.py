import datetime

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.conf import settings

from rest_framework.decorators import list_route
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from user_resource.models import InstituteAddress

class InternalViewset(viewsets.GenericViewSet):

    renderer_classes = (JSONRenderer, )

    @method_decorator(csrf_exempt)
    @list_route(methods=['POST'])
    def searchhostel(self, request):
        if 'secret' not in request.data or request.data['secret'] not in settings.INTERNAL_SECRETS:
            return Response({})

        queryset = InstituteAddress.objects.filter(hostel=request.data['hostel'])
        queryset = queryset.filter(
            Q(user__program__graduation_year__isnull=False) &
            Q(user__program__graduation_year__gte=int(datetime.datetime.now().year))
        )
        queryset = queryset.filter(
            Q(user__first_name__icontains=request.data['search']) |
            Q(user__last_name__icontains=request.data['search']) |
            Q(room__icontains=request.data['search'])
        )
        queryset = queryset.prefetch_related("user")

        return Response([{
            "username": x.user.username,
            "name": "%s %s" % (x.user.first_name , x.user.last_name),
            "hostel": x.hostel,
            "room": x.room
        } for x in queryset])

