from braces.views import LoginRequiredMixin
from django.views.generic import UpdateView
from oauth2_provider.exceptions import OAuthToolkitError
#from oauth2_provider.http import HttpResponseUriRedirect
from oauth2_provider.models import get_application_model as get_oauth2_application_model
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views import AuthorizationView
from oauth2_provider.views.application import ApplicationRegistration

from core.utils import get_default_scopes

from .forms import RegistrationForm


class ApplicationRegistrationView(ApplicationRegistration):
    form_class = RegistrationForm


class ApplicationUpdateView(LoginRequiredMixin, UpdateView):
    """
    View used to update an application owned by the request.user
    """
    form_class = RegistrationForm
    context_object_name = 'application'
    template_name = "oauth2_provider/application_form.html"

    def get_queryset(self):
        return get_oauth2_application_model().objects.filter(user=self.request.user)


class CustomAuthorizationView(AuthorizationView):

    def form_valid(self, form):
        client_id = form.cleaned_data.get('client_id', '')
        application = get_oauth2_application_model().objects.get(client_id=client_id)
        scopes = form.cleaned_data.get('scope', '')
        scopes = set(scopes.split(' '))
        scopes.update(set(get_default_scopes(application)))
        private_scopes = application.private_scopes
        if private_scopes:
            private_scopes = set(private_scopes.split(' '))
            scopes.update(private_scopes)
        scopes = ' '.join(list(scopes))
        form.cleaned_data['scope'] = scopes
        return super(CustomAuthorizationView, self).form_valid(form)

