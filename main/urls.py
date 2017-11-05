from main.views import *
from django.conf.urls import url


urlpatterns = [
    url(r'^register/$', RegisterView.as_view()),
    url(r'^login/$', LoginView.as_view()),
    url(r'^$', homepage),
    url(r'^logout$', logout_view),
    url(r'^search$', beersearch),
    url(r'^api/mark$', apimark),
    url(r'^(?P<name>[\w-]+)/$', make_url.as_view()),
]
