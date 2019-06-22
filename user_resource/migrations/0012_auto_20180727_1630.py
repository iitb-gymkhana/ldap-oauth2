# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_resource', '0011_auto_20151109_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalprogram',
            name='department',
            field=models.CharField(blank=True, max_length=16, null=True, choices=[[b'AE', b'Aerospace Engineering'], [b'ANIM', b'Animation'], [b'ASC', b'Application Software Centre'], [b'AGP', b'Applied Geophysics'], [b'ASI', b'Applied Statistics and Informatics'], [b'BME', b'Biomedical Engineering'], [b'BB', b'Biosciences and Bioengineering'], [b'BIOTECH', b'Biotechnology'], [b'CASDE', b'Centre for Aerospace Systems Design and Engineering'], [b'CDEEP', b'Centre for Distance Engineering Education Programme'], [b'CESE', b'Centre for Environmental Science and Engineering'], [b'CFDVS', b'Centre for Formal Design and Verification of Software'], [b'CRNTS', b'Centre for Research in Nanotechnology and Science'], [b'CTARA', b'Centre for Technology Alternatives for Rural Areas'], [b'CUSE', b'Centre for Urban Science and Engineering'], [b'CSRE', b'Centre of Studies in Resources Engineering'], [b'CHE', b'Chemical Engineering'], [b'CH', b'Chemistry'], [b'CLE', b'Civil Engineering'], [b'CLS', b'Climate Studies'], [b'CC', b'Computer Centre'], [b'CSE', b'Computer Science & Engineering'], [b'CEP', b'Continuing Education Programme'], [b'CORRSCI', b'Corrosion Science and Engineering'], [b'DSCE', b'Desai Sethi Centre for Entrepreneurship'], [b'ES', b'Earth Sciences'], [b'ET', b'Educational Technology'], [b'EE', b'Electrical Engineering'], [b'ESE', b'Energy Science and Engineering'], [b'HSS', b'Humanities & Social Science'], [b'IITBMRA', b'IITB-Monash Research Academy'], [b'IDC', b'Industrial Design Centre'], [b'IDC', b'Industrial Design Centre'], [b'IEOR', b'Industrial Engineering and Operations Research'], [b'IM', b'Industrial Management'], [b'IxD', b'Interaction Design'], [b'KReSIT', b'Kanwal Rekhi School of Information Technology'], [b'MS', b'Material Science'], [b'MMM', b'Materials, Manufacturing and Modelling'], [b'MM', b'Mathematics'], [b'ME', b'Mechanical Engineering'], [b'MEMS', b'Metallurgical Engineering & Materials Science'], [b'MVD', b'Mobility and Vehicle Design'], [b'NCAIR', b'National Centre for Aerospace Innovation and Research'], [b'NCM', b'National Centre for Mathematics'], [b'PHE', b'Physical Education'], [b'PH', b'Physics'], [b'PMS', b'Physics, Material Science'], [b'PC', b'Preparatory Course'], [b'RE', b'Reliability Engineering'], [b'SJMSOM', b'Shailesh J. Mehta School of Management'], [b'SAIF', b'Sophisticated Analytical Instrument Facility'], [b'SCE', b'Systems and Control Engineering'], [b'TCTD', b'Tata Center for Technology and Design'], [b'VISCOM', b'Visual Communication'], [b'WRCB', b'Wadhwani Research Centre for Bioengineering']]),
        ),
    ]
