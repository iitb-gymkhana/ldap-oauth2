import collections
import re

import six
from django.conf import settings
from django.urls import reverse
from django.db.models import Model
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _


def get_default_scopes(application):
    if application.is_anonymous:
        return application.required_scopes.split()
    return settings.OAUTH2_DEFAULT_SCOPES


def attr_to_dict(instance, key=None):
    """
    Convert an instance to dictionary by following rules:
    1. If instance is model then covert it directly to dictionary using forms.model_to_dict
    2. If instance is dictionary or dict like object, return it
    3. If instace is string type or list type, return {key: instance}
    :param instance: A python object
    :param key: @str
    :return: @dict
    """
    if isinstance(instance, Model):
        return model_to_dict(instance)
    if isinstance(instance, collections.Mapping):
        return instance
    if isinstance(instance, six.string_types):
        assert key is not None, _('Key cannot be None when instance is not a Model or collections.Mapping type')
        return {key: instance}


def get_choices_with_blank_dash(choices):
    return BLANK_CHOICE_DASH + list(choices)


SEXES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

DISCIPLINES = [
    # Departments
    ['AE', 'Aerospace Engineering'],
    ['BB', 'Biosciences and Bioengineering'],
    ['CHE', 'Chemical Engineering'],
    ['CH', 'Chemistry'],
    ['CLE', 'Civil Engineering'],
    ['CSE', 'Computer Science & Engineering'],
    ['ES', 'Earth Sciences'],
    ['EE', 'Electrical Engineering'],
    ['ESE', 'Energy Science and Engineering'],
    ['HSS', 'Humanities & Social Science'],
    ['IDC', 'Industrial Design Centre'],
    ['MM', 'Mathematics'],
    ['ME', 'Mechanical Engineering'],
    ['MEMS', 'Metallurgical Engineering & Materials Science'],
    ['PH', 'Physics'],
    ['MS', 'Material Science'],
    ['PHE', 'Physical Education'],
    ['PMS', 'Physics, Material Science'],
    ['PC', 'Preparatory Course'],
    ['RE', 'Reliability Engineering'],

    # Centers
    ['ASC', 'Application Software Centre'],
    ['CRNTS', 'Centre for Research in Nanotechnology and Science'],
    ['CASDE', 'Centre for Aerospace Systems Design and Engineering'],
    ['CC', 'Computer Centre'],
    ['CDEEP', 'Centre for Distance Engineering Education Programme'],
    ['CESE', 'Centre for Environmental Science and Engineering'],
    ['CSRE', 'Centre of Studies in Resources Engineering'],
    ['CTARA', 'Centre for Technology Alternatives for Rural Areas'],
    ['CFDVS', 'Centre for Formal Design and Verification of Software'],
    ['CUSE', 'Centre for Urban Science and Engineering'],
    ['DSCE', 'Desai Sethi Centre for Entrepreneurship'],
    ['IITBMRA', 'IITB-Monash Research Academy'],
    ['NCAIR', 'National Centre for Aerospace Innovation and Research'],
    ['NCM', 'National Centre for Mathematics'],
    ['SAIF', 'Sophisticated Analytical Instrument Facility'],
    ['TCTD', 'Tata Center for Technology and Design'],
    ['WRCB', 'Wadhwani Research Centre for Bioengineering'],
    ['BIOTECH', 'Biotechnology'],
    ['CPS', 'Centre for Policy Studies'],

    # School
    ['SJMSOM', 'Shailesh J. Mehta School of Management'],
    ['KReSIT', 'Kanwal Rekhi School of Information Technology'],

    # Interdisciplinary Programs
    ['CLS', 'Climate Studies'],
    ['ET', 'Educational Technology'],
    ['IEOR', 'Industrial Engineering and Operations Research'],
    ['SCE', 'Systems and Control Engineering'],

    # IDC
    ['ANIM', 'Animation'],
    ['IDC', 'Industrial Design Centre'],
    ['IxD', 'Interaction Design'],
    ['MVD', 'Mobility and Vehicle Design'],
    ['VISCOM', 'Visual Communication'],

    # Others
    ['IM', 'Industrial Management'],
    ['MMM', 'Materials, Manufacturing and Modelling'],
    ['CORRSCI', 'Corrosion Science and Engineering'],
    ['CEP', 'Continuing Education Programme'],
    ['AGP', 'Applied Geophysics'],
    ['ASI', 'Applied Statistics and Informatics'],
    ['BME', 'Biomedical Engineering'],
]

SORTED_DISCIPLINES = sorted(DISCIPLINES, key=lambda x: x[1])

DEGREES = [
    ['BTECH', 'Bachelor of Technology'],
    ['MTECH', 'Master of Technology'],
    ['DD', 'B.Tech. + M.Tech. Dual Degree'],
    ['MSC', 'Master of Science'],
    ['PHD', 'Doctor of Philosophy'],
    ['BDES', 'Bachelor of Design'],
    ['MDES', 'Master of Design'],
    ['MPHIL', 'Master of Philosophy'],
    ['MMG', 'Master of Management'],
    ['MSEx', 'M.S. (Exit Degree)'],
    ['MtechEx', 'Master of Technology (Exit Degree)'],
    ['MtechPhDDD', 'M.Tech. + Ph.D. Dual Degree'],
    ['PC', 'Preparatory Course'],
    ['VS', 'Visiting Student'],
    ['MPhilEx', 'Master of Philosophy (Exit Degree)'],
    ['MScEx', 'Master of Science (Exit Degree)'],
    ['MScMTechDD', 'M.Sc. + M.Tech. Dual Degree'],
    ['MScPhDDD', 'M.Sc. + Ph.D. Dual Degree'],
    ['MPhilPhDDD', 'M.Phil. + Ph.D. Dual Degree'],
    ['EMBA', 'Executive MBA'],
    ['FYBS', 'Four Year BS'],
    ['IMTECH', 'Integrated M.Tech.'],
    ['MSCBR', 'Master of Science By Research'],
    ['TYMSC', 'Two Year M.Sc.'],
    ['FYIMSC', 'Five Year Integrated M.Sc.'],
    ['DIIT', 'D.I.I.T.'],
    ['DIITEx', 'D.I.T.T. (Exit Degree)'],
]

HOSTELS = [
    ['1', 'Hostel 1'],
    ['2', 'Hostel 2'],
    ['3', 'Hostel 3'],
    ['4', 'Hostel 4'],
    ['5', 'Hostel 5'],
    ['6', 'Hostel 6'],
    ['7', 'Hostel 7'],
    ['8', 'Hostel 8'],
    ['9', 'Hostel 9'],
    ['10', 'Hostel 10'],
    ['11', 'Hostel 11'],
    ['12', 'Hostel 12'],
    ['13', 'Hostel 13'],
    ['14', 'Hostel 14'],
    ['15', 'Hostel 15'],
    ['16', 'Hostel 16'],
    ['18', 'Hostel 18'],
    ['tansa', 'Tansa'],
    ['qip', 'QIP'],
]

HOSTELS_WITH_WINGS = ['10', '11', '12', '13', '14', '15', '16']

ROOM_VALIDATION_REGEX = re.compile(r'[A-Z]-\d+')


class TabNav(object):
    def __init__(self, tab, name=None, template_name=None, base_url=None, is_default=False):
        if not tab or not base_url:
            raise ValueError('tab and base_url cannot be None')
        self.tab = tab
        if not name:
            self.name = tab.title()
        else:
            self.name = name
        if not template_name:
            self.template_name = '%s.html' % tab
        else:
            self.template_name = template_name
        self.is_default = is_default
        self.base_url = base_url
        self.is_active = False

    @property
    def url(self):
        if not self.is_default:
            return reverse(self.base_url, args=[self.tab])
        return reverse(self.base_url)

    @property
    def tab_name(self):
        if not self.is_default:
            return self.tab
        return ''
