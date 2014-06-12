from django.conf.urls import patterns, include, url

from django.contrib import admin

from tranquil.contexts import BaseContext
from tranquil.django import context_class_to_view

from example_app.contexts import RootContext

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/', context_class_to_view(RootContext)),
    url(r'^admin/', include(admin.site.urls)),
)
