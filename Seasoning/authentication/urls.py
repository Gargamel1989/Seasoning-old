"""
Copyright 2012, 2013 Driesen Joep

This file is part of Seasoning.

Seasoning is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Seasoning is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Seasoning.  If not, see <http://www.gnu.org/licenses/>.
    
"""
from django.conf.urls import patterns, url
from authentication.views import registration_complete, registration_closed,\
    resend_activation_email, register, activate, change_email,\
    change_password, login
from authentication.backends import RegistrationBackend

urlpatterns = patterns('',
    
    # Registration urls                   
    url(r'^register/$', register, {'backend': RegistrationBackend},
        name='registration'),
    url(r'^register/closed/$', registration_closed,
        name='registration_disallowed'),
    url(r'^register/complete/$', registration_complete,
        name='registration_complete'),
    
    # Activation urls
    url(r'^activate/resend/$', resend_activation_email,
        name='resend_activation_email'),
    url(r'^activate/(?P<activation_key>\w+)/$', activate, {'backend': RegistrationBackend},
        name='registration_activate'),
    
    # Login urls
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'authentication/logout.html'}),
    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset', 
        {'template_name':'authentication/password_reset_form.html',
         'email_template_name':'authentication/password_reset_email.html',
         'subject_template_name':'authentication/password_reset_subject.txt'},
        name='password_reset'),
    url(r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done', 
        {'template_name':'authentication/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name':'authentication/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete', 
        {'template_name':'authentication/password_reset_complete.html'},
        name='password_reset_complete'),
    
    # Profile urls
    url(r'^account/settings/$', 'authentication.views.account_settings'),
    url(r'^account/delete/$', 'authentication.views.account_delete'),
    url(r'^password/change/$', change_password,
        name='password_change'),
    url(r'^email/change/(?P<activation_key>\w+)/$', change_email),
    
    # Social logins
    url(r'^auth/fb/register/', 'authentication.views.facebook_registration'),
    url(r'^auth/fb/connect/', 'authentication.views.facebook_connect'),
    url(r'^auth/fb/channel/$', 'authentication.views.facebook_channel_file'),
    url(r'^auth/fb/', 'authentication.views.facebook_authentication'),
    url(r'^auth/twitter/$', 'authentication.views.twitter_authentication'),
    url(r'^auth/google/$', 'authentication.views.google_authentication'),
    url(r'^auth/openid/$', 'authentication.views.openid_authentication'),
)
