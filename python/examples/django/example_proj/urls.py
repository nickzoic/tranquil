from django.conf.urls import patterns, include, url

from django.contrib import admin

from tranquil.contexts import BaseContext
from tranquil.django import context_class_to_view

import example_app.views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/', example_app.views.api_view),
    url(r'^admin/', include(admin.site.urls)),
)
