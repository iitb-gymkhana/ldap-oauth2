import requests
import base64
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.models import User
from account.models import UserProfile
from django.utils.http import urlencode
from django.urls import set_script_prefix

from core.mixins import SensitivePostParametersMixin

from .forms import LoginForm

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus


class LoginView(SensitivePostParametersMixin, View):
    """
    GET: If user is already logged in then redirect to 'next' parameter in query_params
        Else render the login form
    POST:
        Validate form, login user
    """
    form_class = LoginForm
    template_name = 'account/login.html'

    def get(self, request):
        if not request.META['SCRIPT_NAME']:
            set_script_prefix('/profiles/')

        uhome = request.build_absolute_uri(reverse('user:home'))
        endpoint = uhome + 'redir'
        current_url = request.resolver_match.url_name

        return render(request, self.template_name, {
            'form': self.form_class,
            'usso_url': endpoint + '?' + urlencode({'logout': request.build_absolute_uri(uhome)}),
            'usso_base': settings.USSO_BASE,
            'usso_widget': settings.USSO_RU,
        })

    def post(self, request):
        next_ = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
        return redirect(next_)

class LogoutView(View):
    def get(self, request):
        logout(request)

        usso_redir = reverse('user:home') + 'redir?'

        next_ = request.GET.get('next')
        login_url = reverse('account:login')
        redirect_to = login_url

        if next_ is not None:
            next_ = quote_plus(next_)
            redirect_to = '%s?next=%s' % (login_url, next_) if next_ else login_url

        if settings.USSO_RU:
            return HttpResponseRedirect(usso_redir + urlencode({'logout': request.build_absolute_uri(redirect_to)}))

        return HttpResponseRedirect(redirect_to)

from django.db.models.signals import pre_save

def user_save(sender, instance, *args, **kwargs):
    instance.last_name = instance.last_name[:28]
    instance.first_name = instance.first_name[:28]

pre_save.connect(user_save, sender=User)
