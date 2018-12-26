"""amy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from workshops.views import logout_then_login_with_msg

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='dispatch')),
    path('admin/', admin.site.urls),
]

if settings.ENABLE_PYDATA:
    PyData_urlpatterns = [
        path('workshops/', include('pydata.urls')),
    ]
    urlpatterns += PyData_urlpatterns

urlpatterns += [
    path('api/v1/', include('api.urls')),  # REST API v1
    path('dashboard/', include('dashboard.urls')),
    path('requests/', include('extrequests.urls')),
    path('forms/', include('extforms.urls')),  # external, anonymous user-accessible forms
    path('fiscal/', include('fiscal.urls')),
    path('reports/', include('reports.urls')),
    path('trainings/', include('trainings.urls')),
    path('workshops/', include('workshops.urls')),
    path('select_lookups/', include('workshops.lookups')),  # autocomplete lookups

    # django views for authentication
    path('account/login/',
         auth_views.LoginView.as_view(
             template_name="account/login.html",
             extra_context={"title": "Log in"},
         ),
         name='login'),

    path('account/logout/',
         logout_then_login_with_msg,
         name='logout'),

    path('account/password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name="account/password_reset.html",
         ),
         name='password_reset'),

    path('account/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="account/password_reset_done.html",
         ),
         name='password_reset_done'),

    re_path(r'^account/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
            r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(
                template_name="account/password_reset_confirm.html",
            ),
            name='password_reset_confirm'),

    path('account/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="account/password_reset_complete.html",
         ),
         name='password_reset_complete'),

    # Login with GitHub credentials
    path('', include('social_django.urls', namespace='social')),

    # for commenting system
    path('comments/', include('django_comments.urls')),
]

redirect_urlpatterns = [
    path('workshops/', RedirectView.as_view(pattern_name='dispatch')),
    path('workshops/admin-dashboard/', RedirectView.as_view(pattern_name='admin-dashboard')),
    path('workshops/trainee-dashboard/', RedirectView.as_view(pattern_name='trainee-dashboard')),
    path('workshops/trainee-dashboard/training_progress/', RedirectView.as_view(pattern_name='training-progress')),
    path('workshops/autoupdate_profile/', RedirectView.as_view(pattern_name='autoupdate_profile')),

    path('workshops/training_requests/', RedirectView.as_view(pattern_name='all_trainingrequests')),
    path('workshops/training_requests/merge', RedirectView.as_view(pattern_name='trainingrequests_merge')),
    path('workshops/bulk_upload_training_request_scores', RedirectView.as_view(pattern_name='bulk_upload_training_request_scores')),
    path('workshops/bulk_upload_training_request_scores/confirm', RedirectView.as_view(pattern_name='bulk_upload_training_request_scores_confirmation')),

    path('workshops/workshop_requests/', RedirectView.as_view(pattern_name='all_workshoprequests')),
    path('workshops/requests/', RedirectView.as_view(pattern_name='all_eventrequests')),
    path('workshops/dc_selforganized_requests/', RedirectView.as_view(pattern_name='all_dcselforganizedeventrequests')),
    path('workshops/submissions/', RedirectView.as_view(pattern_name='all_eventsubmissions')),
    path('workshops/profile_updates/', RedirectView.as_view(pattern_name='all_profileupdaterequests')),
    path('workshops/invoices/', RedirectView.as_view(pattern_name='all_invoicerequests')),

    path('workshops/organizations/', RedirectView.as_view(pattern_name='all_organizations')),
    path('workshops/memberships/', RedirectView.as_view(pattern_name='all_memberships')),

    path('workshops/reports/instructors_by_date/', RedirectView.as_view(pattern_name='instructors_by_date')),
    path('workshops/reports/workshops_over_time/', RedirectView.as_view(pattern_name='workshops_over_time')),
    path('workshops/reports/learners_over_time/', RedirectView.as_view(pattern_name='learners_over_time')),
    path('workshops/reports/instructors_over_time/', RedirectView.as_view(pattern_name='instructors_over_time')),
    path('workshops/reports/instructor_num_taught/', RedirectView.as_view(pattern_name='instructor_num_taught')),
    path('workshops/reports/all_activity_over_time/', RedirectView.as_view(pattern_name='all_activity_over_time')),
    path('workshops/reports/membership_trainings_stats/', RedirectView.as_view(pattern_name='membership_trainings_stats')),
    path('workshops/reports/workshop_issues/', RedirectView.as_view(pattern_name='workshop_issues')),
    path('workshops/reports/instructor_issues/', RedirectView.as_view(pattern_name='instructor_issues')),
    path('workshops/reports/duplicate_persons/', RedirectView.as_view(pattern_name='duplicate_persons')),
    path('workshops/reports/duplicate_training_requests/', RedirectView.as_view(pattern_name='duplicate_training_requests')),

    path('workshops/trainings/', RedirectView.as_view(pattern_name='all_trainings')),
    path('workshops/trainees/', RedirectView.as_view(pattern_name='all_trainees')),

    # old form addresses below, to be removed in future
    path('workshops/swc/request/', RedirectView.as_view(pattern_name='swc_workshop_request', permanent=True)),
    path('workshops/swc/request/confirm/', RedirectView.as_view(pattern_name='swc_workshop_request_confirm', permanent=True)),
    path('workshops/dc/request/', RedirectView.as_view(pattern_name='dc_workshop_request', permanent=True)),
    path('workshops/dc/request/confirm/', RedirectView.as_view(pattern_name='dc_workshop_request_confirm', permanent=True)),
    path('workshops/dc/request_selforganized/', RedirectView.as_view(pattern_name='dc_workshop_selforganized_request', permanent=True)),
    path('workshops/dc/request_selforganized/confirm/', RedirectView.as_view(pattern_name='dc_workshop_selforganized_request_confirm', permanent=True)),
    path('workshops/submit/', RedirectView.as_view(pattern_name='event_submit', permanent=True)),
    path('workshops/update_profile/', RedirectView.as_view(pattern_name='profileupdate_request', permanent=True)),
    path('workshops/request_training/', RedirectView.as_view(pattern_name='training_request', permanent=True)),
]

urlpatterns += redirect_urlpatterns

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
