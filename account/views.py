import requests
import base64
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.models import User
from account.models import UserProfile

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
        form = self.form_class(request.POST)
        next_ = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
        if next_ == '':
            next_ = settings.LOGIN_REDIRECT_URL
        if request.user.is_authenticated():
            return redirect(next_)

        code_ = request.GET.get('code', '')
        if code_ != '':
            post_data = 'code=' + code_ + '&redirect_uri=' + settings.USSO_REDIRECT_URI + '&grant_type=authorization_code'

            # Get our access token
            response = requests.post(
                settings.USSO_BASE + '/token',
                data=post_data,
                headers={
                    "Authorization": "Basic " + settings.USSO_CLIENT_ID_SECRET,
                    "Content-Type": "application/x-www-form-urlencoded"
                }, verify=False)
            response_json = response.json()

            # Check that we have the access token
            if 'access_token' not in response_json:
                 form.add_error(None, "Unable to authorize user. Try again!")
                 return render(request, self.template_name, {'form': form})

            # Get the user's profile
            profile_response = requests.get(
                settings.USSO_BASE + '/user',
                headers={
                   "Authorization": "Bearer " + response_json['access_token'],
                }, verify=False)
            profile_json = profile_response.json()

            user = User.objects.filter(userprofile__roll_number=profile_json['employeeNumber']).last()
            if not user:
                user = User.objects.create(
                    username=profile_json['id'],
                    email=profile_json['mail'],
                    first_name=profile_json['givenName'],
                    last_name=profile_json['sn'],
                )
                profile = UserProfile.objects.create(
                    user=user,
                    roll_number=profile_json['employeeNumber'],
                    type=profile_json['employeeType']
                )
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            request.session.set_expiry(0)
            login(request, user)
            return redirect(base64.b64decode(request.GET.get('state', base64.b64encode(next_))))

        return render(request, self.template_name, {
            'form': self.form_class,
            'usso_url': settings.USSO_BASE + '/authorize?state=' + base64.b64encode(next_) + '&response_type=code&approval_prompt=auto&client_id=' + settings.USSO_CLIENT_ID + '&redirect_uri=' + settings.USSO_REDIRECT_URI
        })


    def post(self, request):
        form = self.form_class(request.POST)
        next_ = request.POST.get('next', settings.LOGIN_REDIRECT_URL)
        if next_ == '':
            next_ = settings.LOGIN_REDIRECT_URL
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']

            user = authenticate(username=username, password=password)
            if user is not None:
                if remember:
                    # Yearlong Session
                    request.session.set_expiry(24 * 365 * 3600)
                else:
                    request.session.set_expiry(0)
                login(request, user)
                return redirect(next_)
            else:
                form.add_error(None, "Unable to authorize user. Try again!")
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        next_ = request.GET.get('next')
        if next_ is None:
            return redirect('index')
        next_ = quote_plus(next_)
        login_url = reverse('account:login')
        redirect_to = '%s?next=%s' % (login_url, next_) if next_ else login_url
        return HttpResponseRedirect(redirect_to)
